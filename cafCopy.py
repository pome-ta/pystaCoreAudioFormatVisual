from pathlib import Path

SIMToolkitNegativeACK_path_str = '/System/Library/Audio/UISounds/SIMToolkitNegativeACK.caf'
SIMToolkitNegativeACK_path = Path(SIMToolkitNegativeACK_path_str)

sound_bytes = SIMToolkitNegativeACK_path.read_bytes()

empty_new = Path('./dist/SIMToolkitNegativeACK.caf')

if not empty_new.exists():
  empty_new.touch()

if __name__ == '__main__':
  empty_new.write_bytes(sound_bytes)


