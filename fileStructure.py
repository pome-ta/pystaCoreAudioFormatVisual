from pathlib import Path
import ctypes

import struct

SIMToolkitNegativeACK_path_str = '/System/Library/Audio/UISounds/SIMToolkitNegativeACK.caf'
SIMToolkitNegativeACK_path = Path(SIMToolkitNegativeACK_path_str)

sound_bytes = SIMToolkitNegativeACK_path.read_bytes()


class CAFFileHeader(ctypes.Structure):
  _fields_ = [
    ('mFileType', ctypes.c_uint32),
    ('mFileVersion', ctypes.c_uint16),
    ('mFileFlags', ctypes.c_uint16),
  ]


class CAFChunkHeader(ctypes.Structure):
  _fields_ = [
    ('mChunkType', ctypes.c_uint32),
    ('mChunkSize', ctypes.c_int64),
  ]


class CAFAudioFormat(ctypes.Structure):
  _fields_ = [
    ('mSampleRate', ctypes.c_double),
    ('mFormatID', ctypes.c_uint32),
    ('mFormatFlags', ctypes.c_uint32),
    ('mBytesPerPacket', ctypes.c_uint32),
    ('mFramesPerPacket', ctypes.c_uint32),
    ('mChannelsPerFrame', ctypes.c_uint32),
    ('mBitsPerChannel', ctypes.c_uint32),
  ]


f = ctypes.sizeof(CAFFileHeader)
c = ctypes.sizeof(CAFChunkHeader)
a = ctypes.sizeof(CAFAudioFormat)

print(f, c, a)
h = f + c + a

structs = sound_bytes[:h]

#cafFileHeader = structs[:f]
#cafChunkHeader = structs[f:f + c]
#cafAudioFormat = structs[f + c:f + c + a]
#print(cafFileHeader, ':CAFFileHeader')
#print(cafChunkHeader, ':CAFChunkHeader')
#print(cafAudioFormat, ':CAFAudioFormat')

#print(ctypes.sizeof(ctypes.c_uint16), 'uint16')
#print(ctypes.sizeof(ctypes.c_uint32), 'uint32')
#print(ctypes.sizeof(ctypes.c_int64), 'int64')
print(ctypes.sizeof(ctypes.c_double), 'double')

#mChunkSize = b'\x00\x00\x00\x00\x00\x00\x00 @\xd5\x88\x80'

UInt16 = ctypes.sizeof(ctypes.c_uint16)
UInt32 = ctypes.sizeof(ctypes.c_uint32)
SInt64 = ctypes.sizeof(ctypes.c_int64)
Float64 = ctypes.sizeof(ctypes.c_double)

ff = UInt32 + UInt16 + UInt16
cc = UInt32 + SInt64
aa = Float64 + UInt32 + UInt32 + UInt32 + UInt32 + UInt32 + UInt32

cafFileHeader = structs[:ff]
cafChunkHeader = structs[ff:ff + cc]
cafAudioFormat = structs[ff + cc:ff + cc + aa]


print(cafFileHeader, ':CAFFileHeader')
print(cafChunkHeader, ':CAFChunkHeader')
print(cafAudioFormat, ':CAFAudioFormat')
mChunkType = cafChunkHeader[:UInt32]
mChunkSize = cafChunkHeader[UInt32:]
mSampleRate = cafAudioFormat[:Float64]

#longlong = struct.pack('q', 1)

#print(ctypes.c_uint32(caf))

print(struct.unpack('q', mChunkSize), ':mChunkSize')
print(struct.unpack('d', mSampleRate), ':mSampleRate')
#print(ctypes.sizeof(ctypes.c_longlong))
'''
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

'''

