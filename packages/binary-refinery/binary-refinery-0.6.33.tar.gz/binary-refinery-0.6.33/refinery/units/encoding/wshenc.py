#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

from refinery.units import Arg, Unit
from refinery.lib.patterns import formats


class wshenc(Unit):
    """
    Windows Scripting Host encoding and decoding of VBScript (VBS/VBE) and JScript (JS/JSE).
    """

    _MARKER_INIT = RB'#@~^BINREF=='
    _MARKER_STOP = RB'BINREF==^#~@'

    _CHUNKS = (
        0x57, 0x6E, 0x7B, 0x4A, 0x4C, 0x41, 0x0B, 0x0B, 0x0B, 0x0C, 0x0C, 0x0C, 0x4A, 0x4C, 0x41,
        0x0E, 0x0E, 0x0E, 0x0F, 0x0F, 0x0F, 0x10, 0x10, 0x10, 0x11, 0x11, 0x11, 0x12, 0x12, 0x12,
        0x13, 0x13, 0x13, 0x14, 0x14, 0x14, 0x15, 0x15, 0x15, 0x16, 0x16, 0x16, 0x17, 0x17, 0x17,
        0x18, 0x18, 0x18, 0x19, 0x19, 0x19, 0x1A, 0x1A, 0x1A, 0x1B, 0x1B, 0x1B, 0x1C, 0x1C, 0x1C,
        0x1D, 0x1D, 0x1D, 0x1E, 0x1E, 0x1E, 0x1F, 0x1F, 0x1F, 0x2E, 0x2D, 0x32, 0x47, 0x75, 0x30,
        0x7A, 0x52, 0x21, 0x56, 0x60, 0x29, 0x42, 0x71, 0x5B, 0x6A, 0x5E, 0x38, 0x2F, 0x49, 0x33,
        0x26, 0x5C, 0x3D, 0x49, 0x62, 0x58, 0x41, 0x7D, 0x3A, 0x34, 0x29, 0x35, 0x32, 0x36, 0x65,
        0x5B, 0x20, 0x39, 0x76, 0x7C, 0x5C, 0x72, 0x7A, 0x56, 0x43, 0x7F, 0x73, 0x38, 0x6B, 0x66,
        0x39, 0x63, 0x4E, 0x70, 0x33, 0x45, 0x45, 0x2B, 0x6B, 0x68, 0x68, 0x62, 0x71, 0x51, 0x59,
        0x4F, 0x66, 0x78, 0x09, 0x76, 0x5E, 0x62, 0x31, 0x7D, 0x44, 0x64, 0x4A, 0x23, 0x54, 0x6D,
        0x75, 0x43, 0x71, 0x4A, 0x4C, 0x41, 0x7E, 0x3A, 0x60, 0x4A, 0x4C, 0x41, 0x5E, 0x7E, 0x53,
        0x40, 0x4C, 0x40, 0x77, 0x45, 0x42, 0x4A, 0x2C, 0x27, 0x61, 0x2A, 0x48, 0x5D, 0x74, 0x72,
        0x22, 0x27, 0x75, 0x4B, 0x37, 0x31, 0x6F, 0x44, 0x37, 0x4E, 0x79, 0x4D, 0x3B, 0x59, 0x52,
        0x4C, 0x2F, 0x22, 0x50, 0x6F, 0x54, 0x67, 0x26, 0x6A, 0x2A, 0x72, 0x47, 0x7D, 0x6A, 0x64,
        0x74, 0x39, 0x2D, 0x54, 0x7B, 0x20, 0x2B, 0x3F, 0x7F, 0x2D, 0x38, 0x2E, 0x2C, 0x77, 0x4C,
        0x30, 0x67, 0x5D, 0x6E, 0x53, 0x7E, 0x6B, 0x47, 0x6C, 0x66, 0x34, 0x6F, 0x35, 0x78, 0x79,
        0x25, 0x5D, 0x74, 0x21, 0x30, 0x43, 0x64, 0x23, 0x26, 0x4D, 0x5A, 0x76, 0x52, 0x5B, 0x25,
        0x63, 0x6C, 0x24, 0x3F, 0x48, 0x2B, 0x7B, 0x55, 0x28, 0x78, 0x70, 0x23, 0x29, 0x69, 0x41,
        0x28, 0x2E, 0x34, 0x73, 0x4C, 0x09, 0x59, 0x21, 0x2A, 0x33, 0x24, 0x44, 0x7F, 0x4E, 0x3F,
        0x6D, 0x50, 0x77, 0x55, 0x09, 0x3B, 0x53, 0x56, 0x55, 0x7C, 0x73, 0x69, 0x3A, 0x35, 0x61,
        0x5F, 0x61, 0x63, 0x65, 0x4B, 0x50, 0x46, 0x58, 0x67, 0x58, 0x3B, 0x51, 0x31, 0x57, 0x49,
        0x69, 0x22, 0x4F, 0x6C, 0x6D, 0x46, 0x5A, 0x4D, 0x68, 0x48, 0x25, 0x7C, 0x27, 0x28, 0x36,
        0x5C, 0x46, 0x70, 0x3D, 0x4A, 0x6E, 0x24, 0x32, 0x7A, 0x79, 0x41, 0x2F, 0x37, 0x3D, 0x5F,
        0x60, 0x5F, 0x4B, 0x51, 0x4F, 0x5A, 0x20, 0x42, 0x2C, 0x36, 0x65, 0x57)
    _OFFSETS = (
        0, 1, 2, 0, 1, 2, 1, 2, 2, 1, 2, 1, 0, 2, 1, 2, 0, 2, 1, 2, 0, 0, 1, 2, 2, 1, 0, 2, 1, 2, 2, 1,
        0, 0, 2, 1, 2, 1, 2, 0, 2, 0, 0, 1, 2, 0, 2, 1, 0, 2, 1, 2, 0, 0, 1, 2, 2, 0, 0, 1, 2, 0, 2, 1)
    _ENCODER = {
        0x09 : [0x37, 0x69, 0x64], 0x0B : [0x0B, 0x0B, 0x0B], 0x0C : [0x0C, 0x0C, 0x0C],
        0x0E : [0x0E, 0x0E, 0x0E], 0x0F : [0x0F, 0x0F, 0x0F], 0x10 : [0x10, 0x10, 0x10],
        0x11 : [0x11, 0x11, 0x11], 0x12 : [0x12, 0x12, 0x12], 0x13 : [0x13, 0x13, 0x13],
        0x14 : [0x14, 0x14, 0x14], 0x15 : [0x15, 0x15, 0x15], 0x16 : [0x16, 0x16, 0x16],
        0x17 : [0x17, 0x17, 0x17], 0x18 : [0x18, 0x18, 0x18], 0x19 : [0x19, 0x19, 0x19],
        0x1A : [0x1A, 0x1A, 0x1A], 0x1B : [0x1B, 0x1B, 0x1B], 0x1C : [0x1C, 0x1C, 0x1C],
        0x1D : [0x1D, 0x1D, 0x1D], 0x1E : [0x1E, 0x1E, 0x1E], 0x1F : [0x1F, 0x1F, 0x1F],
        0x20 : [0x7E, 0x2C, 0x50], 0x21 : [0x5A, 0x65, 0x22], 0x22 : [0x45, 0x72, 0x4A],
        0x23 : [0x3A, 0x5B, 0x61], 0x24 : [0x79, 0x66, 0x5E], 0x25 : [0x59, 0x75, 0x5D],
        0x26 : [0x27, 0x4C, 0x5B], 0x27 : [0x76, 0x45, 0x42], 0x28 : [0x63, 0x76, 0x60],
        0x29 : [0x62, 0x2A, 0x23], 0x2A : [0x4D, 0x43, 0x65], 0x2B : [0x51, 0x33, 0x5F],
        0x2C : [0x53, 0x42, 0x7E], 0x2D : [0x52, 0x20, 0x4F], 0x2E : [0x20, 0x63, 0x52],
        0x2F : [0x26, 0x4A, 0x7A], 0x30 : [0x54, 0x5A, 0x21], 0x31 : [0x71, 0x38, 0x46],
        0x32 : [0x2B, 0x79, 0x20], 0x33 : [0x66, 0x32, 0x26], 0x34 : [0x2A, 0x57, 0x63],
        0x35 : [0x58, 0x6C, 0x2A], 0x36 : [0x7F, 0x2B, 0x76], 0x37 : [0x7B, 0x46, 0x47],
        0x38 : [0x30, 0x52, 0x25], 0x39 : [0x31, 0x4F, 0x2C], 0x3A : [0x6C, 0x3D, 0x29],
        0x3B : [0x49, 0x70, 0x69], 0x3D : [0x78, 0x7B, 0x27], 0x3F : [0x5F, 0x51, 0x67],
        0x40 : [0x40, None, 0x40], 0x41 : [0x29, 0x7A, 0x62], 0x42 : [0x24, 0x7E, 0x41],
        0x43 : [0x2F, 0x3B, 0x5A], 0x44 : [0x39, 0x47, 0x66], 0x45 : [0x33, 0x41, 0x32],
        0x46 : [0x6F, 0x77, 0x73], 0x47 : [0x21, 0x56, 0x4D], 0x48 : [0x75, 0x5F, 0x43],
        0x49 : [0x28, 0x26, 0x71], 0x4A : [0x42, 0x78, 0x39], 0x4B : [0x46, 0x6E, 0x7C],
        0x4C : [0x4A, 0x64, 0x53], 0x4D : [0x5C, 0x74, 0x48], 0x4E : [0x48, 0x67, 0x31],
        0x4F : [0x36, 0x7D, 0x72], 0x50 : [0x4B, 0x68, 0x6E], 0x51 : [0x7D, 0x35, 0x70],
        0x52 : [0x5D, 0x22, 0x49], 0x53 : [0x6A, 0x55, 0x3F], 0x54 : [0x50, 0x3A, 0x4B],
        0x55 : [0x69, 0x60, 0x6A], 0x56 : [0x23, 0x6A, 0x2E], 0x57 : [0x09, 0x71, 0x7F],
        0x58 : [0x70, 0x6F, 0x28], 0x59 : [0x65, 0x49, 0x35], 0x5A : [0x74, 0x5C, 0x7D],
        0x5B : [0x2C, 0x5D, 0x24], 0x5C : [0x77, 0x27, 0x2D], 0x5D : [0x44, 0x59, 0x54],
        0x5E : [0x3F, 0x25, 0x37], 0x5F : [0x6D, 0x7C, 0x7B], 0x60 : [0x7C, 0x23, 0x3D],
        0x61 : [0x43, 0x6D, 0x6C], 0x62 : [0x38, 0x28, 0x34], 0x63 : [0x5E, 0x31, 0x6D],
        0x64 : [0x5B, 0x39, 0x4E], 0x65 : [0x6E, 0x7F, 0x2B], 0x66 : [0x57, 0x36, 0x30],
        0x67 : [0x4C, 0x54, 0x6F], 0x68 : [0x34, 0x34, 0x74], 0x69 : [0x72, 0x62, 0x6B],
        0x6A : [0x25, 0x4E, 0x4C], 0x6B : [0x56, 0x30, 0x33], 0x6C : [0x73, 0x5E, 0x56],
        0x6D : [0x68, 0x73, 0x3A], 0x6E : [0x55, 0x09, 0x78], 0x6F : [0x47, 0x4B, 0x57],
        0x70 : [0x32, 0x61, 0x77], 0x71 : [0x35, 0x24, 0x3B], 0x72 : [0x2E, 0x4D, 0x44],
        0x73 : [0x64, 0x6B, 0x2F], 0x74 : [0x4F, 0x44, 0x59], 0x75 : [0x3B, 0x21, 0x45],
        0x76 : [0x2D, 0x37, 0x5C], 0x77 : [0x41, 0x53, 0x68], 0x78 : [0x61, 0x58, 0x36],
        0x79 : [0x7A, 0x48, 0x58], 0x7A : [0x22, 0x2E, 0x79], 0x7B : [0x60, 0x50, 0x09],
        0x7C : [0x6B, 0x2D, 0x75], 0x7D : [0x4E, 0x29, 0x38], 0x7E : [0x3D, 0x3F, 0x55],
        0x7F : [0x67, 0x2F, 0x51]
    }

    _ESCAPE = {
        0x40: B'@$',
        0x3C: B'@!',
        0x3E: B'@*',
        0x0D: B'@#',
        0x0A: B'@&',
    }

    _UNESCAPE = {
        B'@$': B'@',
        B'@!': B'<',
        B'@*': B'>',
        B'@#': B'\r',
        B'@&': B'\n',
    }

    def __init__(
        self,
        marker: Arg.Switch('-m', '--no-marker', off=True, help=(
            'Do not require magic marker when encoding and do not search for '
            'marker when decoding.')
        ) = True
    ):
        super().__init__(marker=marker)

    @classmethod
    def _chunk(cls, byte, index):
        k = byte - 9
        c = cls._CHUNKS[k * 3 : k * 3 + 3]
        return c[cls._OFFSETS[index % 64]]

    def _escape(self, iterable):
        escapes = bytes(self._ESCAPE)
        if self.args.marker:
            yield from self._MARKER_INIT
        for byte in iterable:
            if byte in escapes:
                yield from self._ESCAPE[byte]
            else:
                yield byte
        if self.args.marker:
            yield from self._MARKER_STOP

    def _unescape(self, data):
        def unescaper(m): return self._UNESCAPE[m[0]]
        return re.sub(RB'@[$!*#&]', unescaper, data)

    @classmethod
    def _decoded(cls, data):
        index = -1
        for byte in data:
            if byte < 128:
                index += 1
            if (byte == 9 or 31 < byte < 128) and byte != 60 and byte != 62 and byte != 64:
                byte = cls._chunk(byte, index)
            yield byte

    @classmethod
    def _encoded(cls, data):
        for i, byte in enumerate(data):
            try:
                sequence = cls._ENCODER[byte]
            except KeyError:
                yield byte
            else:
                offset = cls._OFFSETS[i % 0x40]
                yield sequence[offset]

    def reverse(self, data):
        return bytearray(self._escape(self._encoded(data)))

    def process(self, data):
        if self.args.marker:
            match = formats.wshenc.search(data)
            if not match:
                raise ValueError('Encoded script marker was not found.')
            data = match[0][12:-12]
        return bytearray(self._decoded(self._unescape(data)))
