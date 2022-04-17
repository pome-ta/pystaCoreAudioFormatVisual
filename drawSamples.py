from pathlib import Path
import ctypes

'''
path_str = '/System/Library/Audio/UISounds/SIMToolkitNegativeACK.caf'
path_str = '/System/Library/Audio/UISounds/SIMToolkitCallDropped.caf'

#path_str = '/System/Library/Audio/UISounds/New/Bloom.caf'

path = Path(path_str)

sound_bytes = path.read_bytes()
'''

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
  mFileType         : {type_str}
  mFileVersion      : {self.mFileVersion}
  mFileFlags        : {self.mFileFlags}
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
  mChunkType        : {type_str}
  mChunkSize        : {self.mChunkSize}
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
  mSampleRate       : {self.mSampleRate}
  mFormatID         : {id_str}
  mFormatFlags      : {self.mFormatFlags}
  mBytesPerPacket   : {self.mBytesPerPacket}
  mFramesPerPacket  : {self.mFramesPerPacket}
  mChannelsPerFrame : {self.mChannelsPerFrame}
  mBitsPerChannel   : {self.mBitsPerChannel}
    '''

    return str


size_cfh = ctypes.sizeof(CAFFileHeader)
size_cch = ctypes.sizeof(CAFChunkHeader)
size_caf = ctypes.sizeof(CAFAudioFormat)
chunk_cfh = size_cfh
chunk_cch = chunk_cfh + size_cch
chunk_caf = chunk_cch + size_caf


def set_struct(read_path):
  sound_bytes = read_path.read_bytes()
  fixed_header = sound_bytes[:chunk_caf]
  fileHeader = fixed_header[:chunk_cfh]
  chunkHeader = fixed_header[chunk_cfh:chunk_cch]
  audioFormat = fixed_header[chunk_cch:chunk_caf]
  
  cafFileHeader = CAFFileHeader.from_buffer(bytearray(fileHeader))
  
  cafChunkHeader = CAFChunkHeader.from_buffer(bytearray(chunkHeader))
  cafAudioFormat = CAFAudioFormat.from_buffer(bytearray(audioFormat))
  
  
  print(read_path)
  print(cafFileHeader)
  print(cafChunkHeader)
  print(cafAudioFormat)
  print('--- ---- ---')



root_str = '/System/Library/Audio/UISounds/'
root_path = Path(root_str)

all_filepaths = list(root_path.glob('**/*.*'))


for filepath in all_filepaths:
  set_struct(filepath)
  
