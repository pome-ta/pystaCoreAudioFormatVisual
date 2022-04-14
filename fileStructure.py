from pathlib import Path
import ctypes

import struct

SIMToolkitNegativeACK_path_str = '/System/Library/Audio/UISounds/SIMToolkitNegativeACK.caf'
SIMToolkitNegativeACK_path = Path(SIMToolkitNegativeACK_path_str)

sound_bytes = SIMToolkitNegativeACK_path.read_bytes()




class CAFFileHeader(ctypes.BigEndianStructure):
  #class CAFFileHeader(ctypes.Structure):
  _pack_ = 1
  _fields_ = [
    ('mFileType', ctypes.c_uint32),
    ('mFileVersion', ctypes.c_uint16),
    ('mFileFlags', ctypes.c_uint16),
  ]

  def __str__(self):
    # xxx: byte -> int -> byte -> str 🤔
    type_str = self.mFileType.to_bytes(4, 'big').decode()
    str = f'''CAFFileHeader: 
  mFileType\t\t\t: {type_str}
  mFileVersion\t\t: {self.mFileVersion}
  mFileFlags\t\t\t: {self.mFileFlags}
    '''

    return str


class CAFChunkHeader(ctypes.BigEndianStructure):
  #class CAFChunkHeader(ctypes.Structure):
  _pack_ = 1
  _fields_ = [
    ('mChunkType', ctypes.c_uint32),
    ('mChunkSize', ctypes.c_int64),
  ]

  def __str__(self):
    # xxx: byte -> int -> byte -> str 🤔
    type_str = self.mChunkType.to_bytes(4, 'big').decode()
    str = f'''CAFChunkHeader: 
  mChunkType\t\t\t: {type_str}
  mChunkSize\t\t\t: {self.mChunkSize}
    '''

    return str


class CAFAudioFormat(ctypes.BigEndianStructure):
  #class CAFAudioFormat(ctypes.Structure):
  _pack_ = 1
  _fields_ = [
    ('mSampleRate', ctypes.c_double),
    ('mFormatID', ctypes.c_uint32),
    ('mFormatFlags', ctypes.c_uint32),
    ('mBytesPerPacket', ctypes.c_uint32),
    ('mFramesPerPacket', ctypes.c_uint32),
    ('mChannelsPerFrame', ctypes.c_uint32),
    ('mBitsPerChannel', ctypes.c_uint32),
  ]

  def __str__(self):
    # xxx: byte -> int -> byte -> str 🤔
    id_str = self.mFormatID.to_bytes(4, 'big').decode()
    str = f'''CAFAudioFormat: 
  mSampleRate\t\t\t: {self.mSampleRate}
  mFormatID\t\t\t: {id_str}
  mFormatFlags\t\t: {self.mFormatFlags}
  mBytesPerPacket\t: {self.mBytesPerPacket}
  mFramesPerPacket\t: {self.mFramesPerPacket}
  mChannelsPerFrame\t: {self.mChannelsPerFrame}
  mBitsPerChannel\t: {self.mBitsPerChannel}
    '''

    return str


f = ctypes.sizeof(CAFFileHeader)
c = ctypes.sizeof(CAFChunkHeader)
a = ctypes.sizeof(CAFAudioFormat)

print(f, c, a)
h = f + c + a

fileHeader = sound_bytes[:f]
chunkHeader = sound_bytes[f:f + c]
audioFormat = sound_bytes[f + c:f + c + a]

cafFileHeader = CAFFileHeader.from_buffer(bytearray(fileHeader))
cafChunkHeader = CAFChunkHeader.from_buffer(bytearray(chunkHeader))
cafAudioFormat = CAFAudioFormat.from_buffer(bytearray(audioFormat))

print(cafFileHeader)
print(cafChunkHeader)
print(cafAudioFormat)

#print(bytearray(file_header))
'''
#cafFileHeader = structs[:f]
#cafChunkHeader = structs[f:f + c]
#cafAudioFormat = structs[f + c:f + c + a]
#print(cafFileHeader, ':CAFFileHeader')
#print(cafChunkHeader, ':CAFChunkHeader')
#print(cafAudioFormat, ':CAFAudioFormat')

#print(ctypes.sizeof(ctypes.c_uint16), 'uint16')
#print(ctypes.sizeof(ctypes.c_uint32), 'uint32')
#print(ctypes.sizeof(ctypes.c_int64), 'int64')
#print(ctypes.sizeof(ctypes.c_double), 'double')

#mChunkSize = b'\x00\x00\x00\x00\x00\x00\x00 @\xd5\x88\x80'

UInt16 = ctypes.sizeof(ctypes.c_uint16)
UInt32 = ctypes.sizeof(ctypes.c_uint32)
SInt64 = ctypes.sizeof(ctypes.c_int64)
Float64 = ctypes.sizeof(ctypes.c_double)

ff = UInt32 + UInt16 + UInt16
cc = UInt32 + SInt64
aa = Float64 + UInt32 + UInt32 + UInt32 + UInt32 + UInt32 + UInt32

hh = ff + cc + aa

structs = sound_bytes[:hh]

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

print(struct.unpack('>q', mChunkSize), ':mChunkSize')
print(struct.unpack('>d', mSampleRate), ':mSampleRate')
#print(ctypes.sizeof(ctypes.c_longlong))
'''
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


