#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from refinery.units import Arg, Unit
from refinery.lib.tools import splitchunks
from refinery.lib.mscrypto import BCRYPT_RSAKEY_BLOB, CRYPTOKEY, TYPES
from refinery.lib.xml import ForgivingParse

from base64 import b64decode, b16decode
from contextlib import suppress
from enum import IntEnum
from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from Cryptodome.Util import number


def normalize_rsa_key(key: bytes, force_public=False):
    try:
        mod, colon, exp = key.partition(B':')
        if colon == B':':
            mod = number.bytes_to_long(b16decode(mod, casefold=True))
            exp = number.bytes_to_long(b16decode(exp, casefold=True))
            return RSA.construct((mod, exp))
    except Exception:
        pass
    try:
        key = b64decode(key, validate=True)
    except Exception:
        pass
    try:
        dom = ForgivingParse(key)
    except ValueError:
        pass
    else:
        data = {child.tag.upper(): number.bytes_to_long(b64decode(child.text)) for child in dom.getroot()}
        components = (data['MODULUS'], data['EXPONENT'])
        if not force_public:
            if 'D' in data:
                components += data['D'],
            if 'P' in data and 'Q' in data:
                components += data['P'], data['Q']
        return RSA.construct(components)
    try:
        blob = CRYPTOKEY(key)
    except ValueError:
        pass
    else:
        if blob.header.type not in {TYPES.PUBLICKEYBLOB, TYPES.PRIVATEKEYBLOB}:
            raise ValueError(F'The provided key is of invalid type {blob.header.type!s}, the algorithm is {blob.header.algorithm!s}.')
        if force_public and blob.header.type is TYPES.PRIVATEKEYBLOB:
            blob = blob.pub
        return blob.key.convert()
    try:
        blob = BCRYPT_RSAKEY_BLOB(key)
    except ValueError:
        key = RSA.import_key(key)
        if force_public:
            key = key.public_key()
        return key
    else:
        return blob.convert(force_public=force_public)


class PAD(IntEnum):
    AUTO = 0
    NONE = 1
    OAEP = 2
    PKCS15 = 3
    PKCS10 = 4


class rsa(Unit):
    """
    Implements single block RSA encryption and decryption. This unit can be used to encrypt
    and decrypt blocks generated by openssl's `rsautl` tool when using the mode `-verify`.
    When it is executed with a public key for decryption or with a private key for encryption,
    it will perform a raw RSA operation. The result of these operations are (un)padded using
    EMSA-PKCS1-v1_5.
    """
    def __init__(
        self,
        key: Arg(help='RSA key in PEM, DER, or Microsoft BLOB format.'),
        swapkeys: Arg.Switch('-s', help='Swap public and private exponent.') = False,
        textbook: Arg.Switch('-t', group='PAD', help='Equivalent to --padding=NONE.') = False,
        padding : Arg.Option('-p', group='PAD', choices=PAD,
            help='Choose one of the following padding modes: {choices}. The default is AUTO.') = PAD.AUTO,
        rsautl  : Arg.Switch('-r', group='PAD',
            help='Act as rsautl from OpenSSH; This is equivalent to --swapkeys --padding=PKCS10') = False,
    ):
        padding = Arg.AsOption(padding, PAD)
        if textbook:
            if padding != PAD.AUTO:
                raise ValueError('Conflicting padding options!')
            padding = padding.NONE
        if rsautl:
            if padding and padding != PAD.PKCS10:
                raise ValueError('Conflicting padding options!')
            swapkeys = True
            padding = PAD.PKCS10

        super().__init__(key=key, textbook=textbook, padding=padding, swapkeys=swapkeys)

        self._key_hash = None
        self._key_data = None

    @property
    def blocksize(self) -> int:
        return self.key.size_in_bytes()

    @property
    def _blocksize_plain(self) -> int:
        # PKCS#1 v1.5 padding is at least 11 bytes.
        return self.blocksize - 11

    @property
    def pub(self):
        return self.key.d if self.args.swapkeys else self.key.e

    @property
    def prv(self):
        return self.key.e if self.args.swapkeys else self.key.d

    def _get_msg(self, data):
        msg = int.from_bytes(data, byteorder='big')
        if msg > self.key.n:
            raise ValueError(F'This key can only handle messages of size {self.blocksize}.')
        return msg

    def _encrypt_raw(self, data):
        return pow(
            self._get_msg(data),
            self.pub,
            self.key.n
        ).to_bytes(self.blocksize, byteorder='big')

    def _decrypt_raw(self, data):
        return pow(
            self._get_msg(data),
            self.prv,
            self.key.n
        ).to_bytes(self.blocksize, byteorder='big')

    def _unpad(self, data, head, padbyte=None):
        if len(data) > self.blocksize:
            raise ValueError(F'This key can only handle messages of size {self.blocksize}.')
        if data.startswith(head):
            pos = data.find(B'\0', 2)
            if pos > 0:
                pad = data[2:pos]
                if padbyte is None or all(b == padbyte for b in pad):
                    return data[pos + 1:]
        raise ValueError('Incorrect padding')

    def _pad(self, data, head, padbyte=None):
        if len(data) > self._blocksize_plain:
            raise ValueError(F'This key can only encrypt messages of size at most {self._blocksize_plain}.')
        pad = self.blocksize - len(data) - len(head) - 1
        if padbyte is not None:
            padding = pad * bytes((padbyte,))
        else:
            padding = bytearray(1)
            while not all(padding):
                padding = bytearray(filter(None, padding))
                padding.extend(get_random_bytes(pad - len(padding)))
        return head + padding + B'\0' + data

    def _unpad_pkcs10(self, data):
        return self._unpad(data, B'\x00\x01', 0xFF)

    def _unpad_pkcs15(self, data):
        return self._unpad(data, B'\x00\x02', None)

    def _pad_pkcs10(self, data):
        return self._pad(data, B'\x00\x01', 0xFF)

    def _pad_pkcs15(self, data):
        return self._pad(data, B'\x00\x02', None)

    def _decrypt_block_OAEP(self, data):
        self.log_debug('Attempting decryption with PyCrypto PKCS1 OAEP.')
        result = PKCS1_OAEP.new(self.key).decrypt(data)
        if result is not None:
            return result
        raise ValueError('OAEP decryption was unsuccessful.')

    def _encrypt_block_OAEP(self, data):
        self.log_debug('Attempting encryption with PyCrypto PKCS1 OAEP.')
        result = PKCS1_OAEP.new(self.key).encrypt(data)
        if result is None:
            return result
        raise ValueError('OAEP encryption was unsuccessful.')

    def _decrypt_block(self, data):
        if self._oaep and self._pads in {PAD.AUTO, PAD.OAEP}:
            try:
                return self._decrypt_block_OAEP(data)
            except ValueError:
                if self._pads: raise
                self.log_debug('PyCrypto primitives failed, no longer attempting OAEP.')
                self._oaep = False

        data = self._decrypt_raw(data)
        return self._unpad_per_argument(data)

    def _unpad_per_argument(self, data):
        if self._pads == PAD.NONE:
            return data
        elif self._pads == PAD.PKCS10:
            return self._unpad_pkcs10(data)
        elif self._pads == PAD.PKCS15:
            return self._unpad_pkcs15(data)
        elif self._pads == PAD.AUTO:
            with suppress(ValueError):
                data = self._unpad_pkcs10(data)
                self.log_info('Detected PKCS1.0 padding.')
                self._pads = PAD.PKCS10
                return data
            with suppress(ValueError):
                data = self._unpad_pkcs15(data)
                self.log_info('Detected PKCS1.5 padding.')
                self._pads = PAD.PKCS15
                return data
            self.log_warn('No padding worked, returning raw decrypted blocks.')
            self._pads = PAD.NONE
            return data
        else:
            raise ValueError(F'Invalid padding value: {self._pads!r}')

    def _encrypt_block(self, data):
        if self._pads in {PAD.AUTO, PAD.OAEP}:
            try:
                return self._encrypt_block_OAEP(data)
            except ValueError:
                if self._pads: raise
                self.log_debug('PyCrypto primitives for OAEP failed, falling back to PKCS1.5.')
                self._pads = PAD.PKCS15

        if self._pads == PAD.PKCS15:
            data = self._pad_pkcs15(data)
        elif self._pads == PAD.PKCS10:
            data = self._pad_pkcs10(data)

        return self._encrypt_raw(data)

    @property
    def key(self) -> RSA.RsaKey:
        key_blob = self.args.key
        key_hash = hash(key_blob)
        if key_hash != self._key_hash:
            self._key_hash = key_hash
            self._key_data = normalize_rsa_key(key_blob)
        return self._key_data

    def process(self, data):
        self._oaep = True
        self._pads = self.args.padding
        if not self.key.has_private():
            try:
                return self._unpad_per_argument(self._encrypt_raw(data))
            except Exception as E:
                raise ValueError(F'A public key was given for decryption and rsautl mode resulted in an error: {E}') from E
        return B''.join(self._decrypt_block(block) for block in splitchunks(data, self.blocksize))

    def reverse(self, data):
        self._pads = self.args.padding
        return B''.join(self._encrypt_block(block) for block in splitchunks(data, self._blocksize_plain))
