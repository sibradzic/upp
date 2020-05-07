# -*- coding: utf-8 -*-
#
# This is NOT auto-generated structure, it was written manually, in attempt
# to reverse-engineer AMD APU Bristol/Raven Ridge PowerPlay tables
#
import ctypes


class struct__ATOM_COMMON_TABLE_HEADER(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('usStructureSize', ctypes.c_uint16),
    ('ucTableFormatRevision', ctypes.c_ubyte),
    ('ucTableContentRevision', ctypes.c_ubyte),
     ]

class struct__ATOM_APU_POWERPLAYTABLE(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('sHeader', struct__ATOM_COMMON_TABLE_HEADER),
    ('ucTableRevision', ctypes.c_ubyte),
    ('ulUnknownDoubleWord1', ctypes.c_uint32),
    ('usUnknown09TableOffset', ctypes.c_uint16),
    ('usUnknown0bTableOffset', ctypes.c_uint16),
    ('usUnknown0dTableOffset', ctypes.c_uint16),
    ('ulUnknownDoubleWord2', ctypes.c_uint32),
    ('usUnknown09TableOffset', ctypes.c_uint16),
    ('ucUnknownByte', ctypes.c_ubyte * 23),
    ('usUnknown2cTableOffset', ctypes.c_uint16),
    ('ulUnknownDoubleWord', ctypes.c_uint32 * 2),
    ('usUnknown36TableOffset', ctypes.c_uint16),
    ('usReserved?', ctypes.c_uint16 * 5),
     ]

# 0x09:   0x58     0x42    : 0x0202     8 bytes   tbl v2?, 2x 3-byte structure
class struct__ATOM_APU_Unknown09_Record(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('ucUnknownByte1', ctypes.c_ubyte),
    ('ucUnknownByte2', ctypes.c_ubyte),
    ('ucUnknownByte3', ctypes.c_ubyte),
     ]
ATOM_APU_Unknown09_Record = struct__ATOM_APU_Unknown09_Record
class struct__ATOM_APU_Unknown09_Table(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('ucRevId', ctypes.c_ubyte),
    ('ucNumEntries', ctypes.c_ubyte),
    ('entries', struct__ATOM_APU_Unknown09_Record * 1),
     ]
ATOM_APU_Unknown09_Table = struct__ATOM_APU_Unknown09_Table

# 0x0b:   0x60     0x4a    : 0x0804    34 bytes   tbl v8?, 4x 8-byte structure
class struct__ATOM_APU_Unknown0b_Record(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('ucUnknownByte1', ctypes.c_ubyte),
    ('ucUnknownByte2', ctypes.c_ubyte),
    ('ucUnknownByte3', ctypes.c_ubyte),
    ('ucUnknownByte4', ctypes.c_ubyte),
    ('ucUnknownByte5', ctypes.c_ubyte),
    ('ucUnknownByte6', ctypes.c_ubyte),
    ('ucUnknownByte7', ctypes.c_ubyte),
    ('ucUnknownByte8', ctypes.c_ubyte),
     ]
ATOM_APU_Unknown0b_Record = struct__ATOM_APU_Unknown0b_Record
class struct__ATOM_APU_Unknown0b_Table(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('ucRevId', ctypes.c_ubyte),
    ('ucNumEntries', ctypes.c_ubyte),
    ('entries', struct__ATOM_APU_Unknown0b_Record * 1),
     ]
ATOM_APU_Unknown0b_Table = struct__ATOM_APU_Unknown0b_Table

# 0x0d:   0x82     0x6c    : 0x0218    50 bytes   tbl v2?, 24x 2-byte structure?
class struct__ATOM_APU_Unknown0d_Record(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('ucUnknownWord', ctypes.c_uint16),
     ]
ATOM_APU_Unknown0d_Record = struct__ATOM_APU_Unknown0d_Record
class struct__ATOM_APU_Unknown0d_Table(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('ucRevId', ctypes.c_ubyte),
    ('ucNumEntries', ctypes.c_ubyte),
    ('entries', struct__ATOM_APU_Unknown0d_Record * 1),
     ]
ATOM_APU_Unknown0d_Table = struct__ATOM_APU_Unknown0d_Table

# 0x2c:   0xb4     0x9e    : 0x(18|1a) b:24 r:26  another jump table, header byte shows its length in bytes
class struct__ATOM_APU_Unknown2c_Table(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('ucLength?', ctypes.c_ubyte),                # Bristol 24 bytes, Raven 26 bytes
    ('ucPadding?', ctypes.c_ubyte),
    ('usUnknown00TableOffset', ctypes.c_uint16),
    ('usUnknown02TableOffset', ctypes.c_uint16),
    ('usUnknown04TableOffset', ctypes.c_uint16),
    ('usUnknown06TableOffset', ctypes.c_uint16),
    ('usUnknown08TableOffset', ctypes.c_uint16),  # used
    ('usUnknown0aTableOffset', ctypes.c_uint16),  # used
    ('usUnknown0cTableOffset', ctypes.c_uint16),
    ('usUnknown0eTableOffset', ctypes.c_uint16),
    ('usUnknown10TableOffset', ctypes.c_uint16),  # used
    ('usUnknown12TableOffset', ctypes.c_uint16),
    ('usUnknown36TableOffset', ctypes.c_uint16),  # used, same structure (and almost the same values) as Unknown36_Table
#    ('usUnknown16TableOffset', ctypes.c_uint16),  # Only on Raven, but unused
     ]
ATOM_APU_Unknown2c_Table = struct__ATOM_APU_Unknown2c_Table

# 0x36:   0x0173   0xb8    : 0x0830    41 bytes   version-less array: 8x 5-bytes (values almost SAME as in 2nd-level jump-table @ offset 0x16!)
class struct__ATOM_APU_Unknown36_Record(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('ucUnknownWord1', ctypes.c_uint16),
    ('ucUnknownByte1', ctypes.c_ubyte),
    ('ucUnknownByte2', ctypes.c_ubyte),
    ('ucUnknownByte3', ctypes.c_ubyte),
     ]
ATOM_APU_Unknown36_Record = struct__ATOM_APU_Unknown36_Record
class struct__ATOM_APU_Unknown36_Table(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('ucNumEntries', ctypes.c_ubyte),
    ('entries', struct__ATOM_APU_Unknown36_Record * 1),
     ]
ATOM_APU_Unknown36_Table = struct__ATOM_APU_Unknown36_Table

# 0x08:   0xcc     0xe1    : 0x00      b:92 r:98  tbl v0, 3 arrays: (b:8,r:9)x 6-bytes, 8x 3-bytes, 8x 2-bytes
class struct__ATOM_APU_Unknown08_1st_Record(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('ucUnknownWord1', ctypes.c_uint16),
    ('ucUnknownByte1', ctypes.c_ubyte),
    ('ucUnknownWord2', ctypes.c_uint16),
    ('ucUnknownByte2', ctypes.c_ubyte),
     ]
ATOM_APU_Unknown08_1st_Record = struct__ATOM_APU_Unknown08_1st_Record
class struct__ATOM_APU_Unknown08_1st_Table(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('ucNumEntries', ctypes.c_ubyte),
    ('entries', struct__ATOM_APU_Unknown08_1st_Record * 1),
     ]
ATOM_APU_Unknown08_1st_Table = struct__ATOM_APU_Unknown08_1st_Table
class struct__ATOM_APU_Unknown08_2nd_Record(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('ucUnknownByte1', ctypes.c_ubyte),
    ('ucUnknownByte2', ctypes.c_ubyte),
    ('ucUnknownIndex', ctypes.c_ubyte),
     ]
ATOM_APU_Unknown08_2nd_Record = struct__ATOM_APU_Unknown08_2nd_Record
class struct__ATOM_APU_Unknown08_2nd_Table(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('ucNumEntries', ctypes.c_ubyte),
    ('entries', struct__ATOM_APU_Unknown08_2nd_Record * 1),
     ]
ATOM_APU_Unknown08_2nd_Table = struct__ATOM_APU_Unknown08_2nd_Table
class struct__ATOM_APU_Unknown08_3rd_Record(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('ucUnknownByte1', ctypes.c_ubyte),
    ('ucUnknownByte2', ctypes.c_ubyte),
     ]
ATOM_APU_Unknown08_3rd_Record = struct__ATOM_APU_Unknown08_3rd_Record
class struct__ATOM_APU_Unknown08_3rd_Table(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('ucNumEntries', ctypes.c_ubyte),
    ('entries', struct__ATOM_APU_Unknown08_3rd_Record * 1),
     ]
ATOM_APU_Unknown08_3rd_Table = struct__ATOM_APU_Unknown08_3rd_Table
class struct__ATOM_APU_Unknown08_Table(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('ucRevId', ctypes.c_ubyte),
    ('1stArray', struct__ATOM_APU_Unknown08_1st_Table),
    ('2ndArray', struct__ATOM_APU_Unknown08_2nd_Table),
    ('3rdArray', struct__ATOM_APU_Unknown08_3rd_Table),
     ]
ATOM_APU_Unknown08_Table = struct__ATOM_APU_Unknown08_Table

# 0x0a:   0x0128   0x0143  : 0x00      75 bytes   tbl v0, 2 arrays: 8x 6-bytes, 8x 3-bytes
class struct__ATOM_APU_Unknown0a_1st_Record(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('ucUnknownWord1', ctypes.c_uint16),
    ('ucUnknownByte1', ctypes.c_ubyte),
    ('ucUnknownWord2', ctypes.c_uint16),
    ('ucUnknownByte2', ctypes.c_ubyte),
     ]
ATOM_APU_Unknown0a_1st_Record = struct__ATOM_APU_Unknown0a_1st_Record
class struct__ATOM_APU_Unknown0a_1st_Table(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('ucNumEntries', ctypes.c_ubyte),
    ('entries', struct__ATOM_APU_Unknown0a_1st_Record * 1),
     ]
ATOM_APU_Unknown0a_1st_Table = struct__ATOM_APU_Unknown0a_1st_Table
class struct__ATOM_APU_Unknown0a_2nd_Record(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('ucUnknownByte1', ctypes.c_ubyte),
    ('ucUnknownByte2', ctypes.c_ubyte),
    ('ucUnknownIndex', ctypes.c_ubyte),
     ]
ATOM_APU_Unknown0a_2nd_Record = struct__ATOM_APU_Unknown0a_2nd_Record
class struct__ATOM_APU_Unknown0a_2nd_Table(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('ucNumEntries', ctypes.c_ubyte),
    ('entries', struct__ATOM_APU_Unknown0a_2nd_Record * 1),
     ]
ATOM_APU_Unknown0a_2nd_Table = struct__ATOM_APU_Unknown0a_2nd_Table
class struct__ATOM_APU_Unknown0a_Table(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('ucRevId', ctypes.c_ubyte),
    ('1stArray', struct__ATOM_APU_Unknown0a_1st_Table),
    ('2ndArray', struct__ATOM_APU_Unknown0a_2nd_Table),
     ]
ATOM_APU_Unknown0a_Table = struct__ATOM_APU_Unknown0a_Table

# 0x10:   0x019c   0x018e  : 0x00      42 bytes   tbl v0, 1 array: 8x 5-bytes
class struct__ATOM_APU_Unknown10_1st_Record(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('ucUnknownByte1', ctypes.c_ubyte),
    ('ucUnknownByte2', ctypes.c_ubyte),
    ('ucUnknownWord', ctypes.c_uint16),
    ('ucUnknownByte3', ctypes.c_ubyte),
     ]
ATOM_APU_Unknown10_1st_Record = struct__ATOM_APU_Unknown10_1st_Record
class struct__ATOM_APU_Unknown10_1st_Table(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('ucNumEntries', ctypes.c_ubyte),
    ('entries', struct__ATOM_APU_Unknown10_1st_Record * 1),
     ]
ATOM_APU_Unknown10_1st_Table = struct__ATOM_APU_Unknown10_1st_Table
class struct__ATOM_APU_Unknown10_Table(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('ucRevId', ctypes.c_ubyte),
    ('1stArray', struct__ATOM_APU_Unknown10_1st_Table),
     ]
ATOM_APU_Unknown10_Table = struct__ATOM_APU_Unknown10_Table

__all__ = \
    [
    'struct__ATOM_COMMON_TABLE_HEADER',
    'struct__ATOM_APU_POWERPLAYTABLE',

    'ATOM_APU_Unknown09_Record',
    'ATOM_APU_Unknown09_Table',
    'ATOM_APU_Unknown0b_Record',
    'ATOM_APU_Unknown0b_Table',
    'ATOM_APU_Unknown0d_Record',
    'ATOM_APU_Unknown0d_Table',

    'ATOM_APU_Unknown2c_Table',

    'ATOM_APU_Unknown36_Record',
    'ATOM_APU_Unknown36_Table',

    'ATOM_APU_Unknown08_1st_Record',
    'ATOM_APU_Unknown08_1st_Table',
    'ATOM_APU_Unknown08_2nd_Record',
    'ATOM_APU_Unknown08_2nd_Table',
    'ATOM_APU_Unknown08_3rd_Record',
    'ATOM_APU_Unknown08_3rd_Table',
    'ATOM_APU_Unknown08_Table',

    'ATOM_APU_Unknown0a_1st_Record',
    'ATOM_APU_Unknown0a_1st_Table',
    'ATOM_APU_Unknown0a_2nd_Record',
    'ATOM_APU_Unknown0a_2nd_Table',
    'ATOM_APU_Unknown0a_Table',

    'ATOM_APU_Unknown10_1st_Record',
    'ATOM_APU_Unknown10_1st_Table',

    'ATOM_APU_Unknown10_Table'
    ]
