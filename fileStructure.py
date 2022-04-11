from pathlib import Path
import struct
from ctypes import c_uint32, c_uint16, c_longlong, c_double
from ctypes import sizeof
from pprint import pprint

from objc_util import *

SIMToolkitNegativeACK_path_str = '/System/Library/Audio/UISounds/SIMToolkitNegativeACK.caf'
SIMToolkitNegativeACK_path = Path(SIMToolkitNegativeACK_path_str)

sound_bytes = SIMToolkitNegativeACK_path.read_bytes()

s = 0
e = sizeof(c_uint32(0))
mFileType = sound_bytes[s:e]

s = e
e = s + sizeof(c_uint16(0))
mFileVersion = sound_bytes[s:e]
s = e
e = s + sizeof(c_uint16(0))
mFileFlags = sound_bytes[s:e]

s = e
e = s + sizeof(c_uint32(0))
mChunkType = sound_bytes[s:e]

s = e
e = s + sizeof(c_longlong(0))

mChunkSize = sound_bytes[s:e]


s = e
e = s + sizeof(c_double(0))
mSampleRate = sound_bytes[s:e]

s = e
e = s + sizeof(c_uint32(0))
mFormatID = sound_bytes[s:e]


s = e
e = s + sizeof(c_uint32(0))
mFormatFlags = sound_bytes[s:e]

sample = 44800.0
print(struct.pack('<f', sample))
