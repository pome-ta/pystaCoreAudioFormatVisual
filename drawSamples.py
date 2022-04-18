from pathlib import Path
import ctypes

import matplotlib.pyplot as plt

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

# xxx: `cafChunkHeader.mChunkSize` 無視で固定でOk？
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
  
  chunk_dch = chunk_caf + size_cch
  dataChunkHeader = sound_bytes[chunk_caf:chunk_dch]
  audioDataChunkHeader = CAFChunkHeader.from_buffer(bytearray(dataChunkHeader))
  
  
  
  
  if audioDataChunkHeader.mChunkType.to_bytes(4, 'big').decode() == 'data':
    cafaudio_size = audioDataChunkHeader.mChunkSize
    chunk_ads = chunk_dch + cafaudio_size
    
    cafData = sound_bytes[chunk_dch: chunk_ads]
    mEditCount = cafData[:4]
    mData = cafData[4:]
    
    data = byte_to_array(mData, 2)
    if cafAudioFormat.mChannelsPerFrame == 2 and cafAudioFormat.mBytesPerPacket == 4:
      data_l = data[::2]
      data_r = data[1::2]
    elif cafAudioFormat.mChannelsPerFrame == 1 and cafAudioFormat.mBytesPerPacket == 2:
      data_l = data
      data_r = data
    
    
    print(read_path)
    #print(cafFileHeader)
    #print(cafChunkHeader)
    #print(cafAudioFormat)
    #print(audioDataChunkHeader)
    #print(len(cafData))
    #print(chunk_caf, chunk_dch, chunk_dch-chunk_caf)
    #plt.title(f'{read_path}')
    plt.subplot(2, 1, 1)
    plt.plot(data_l, alpha=0.5)
    #plt.plot(data_l)
    plt.subplot(2, 1, 2)
    plt.plot(data_r, alpha=0.5)
    #plt.plot(data_r)
    plt.show()
    plt.close()
    print('--- ---- ---')


def to_int16(mb):
  return int.from_bytes(mb, byteorder='little', signed=True)


def byte_to_array(mbyte, cols):
  return [to_int16(mbyte[b:b + cols]) for b in range(0, len(mbyte), cols)]







root_str = '/System/Library/Audio/UISounds/'
root_path = Path(root_str)

all_filepaths = list(root_path.glob('**/*.*'))


for filepath in all_filepaths:
  set_struct(filepath)
  
