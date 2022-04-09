from pathlib import Path
from io import BytesIO


SIMToolkitNegativeACK_path_str = '/System/Library/Audio/UISounds/SIMToolkitNegativeACK.caf'
SIMToolkitNegativeACK_path = Path(SIMToolkitNegativeACK_path_str)

bytes = SIMToolkitNegativeACK_path.read_bytes()
print(bytes)
