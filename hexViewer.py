from pathlib import Path
import ui

from pprint import pprint

# https://github.com/humberry/hexviewer

FONT = ('Ubuntu Mono', 11.5)
BG_COLOR = .128
TEXT_COLOR = .872
HEX_RANGE = range(16)


def convert_bytes_to_list(bytes, size):
  return [bytes[byte:byte + size] for byte in range(0, len(bytes), size)]


def get_hex_texts(join_str, list=None):
  bytes = list if list else HEX_RANGE
  return join_str.join([format(byte, '02X') for byte in bytes])


def set_hex_str(bytes):
  return_text = ''
  bytes_list = convert_bytes_to_list(bytes, 16)
  for n, byte in enumerate(bytes_list):
    addr_txt = format(n * 16, '04X')
    hex_txt = get_hex_texts(',', byte)
    char_txt = ''.join(
      [chr(c) if 31 < c < 127 else '¯' if 0 == c else '•' for c in byte])
    return_text += f'{addr_txt}| {hex_txt}|{char_txt}\n'
  return return_text

# xxx: うまくまとめたい
def set_header_str(*args):
  hex_txt = get_hex_texts(',')
  char_txt = ''.join([format(c, 'X') for c in HEX_RANGE])
  return f'ADRS| {hex_txt}|{char_txt}'


class HexView(ui.View):
  def __init__(self, path, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    sound_bytes = path.read_bytes()
    self.bg_color = 'slategray'

    self.header_view = self.setup_hex_text(set_header_str)
    self.header_view.flex = 'W'
    self.header_view.scroll_enabled = False

    self.binary_view = self.setup_hex_text(set_hex_str, sound_bytes)
    self.binary_view.flex = 'WH'

    self.add_subview(self.header_view)
    self.add_subview(self.binary_view)

  def setup_hex_text(self, func, var=None):
    text_view = ui.TextView()
    text_view.editable = False
    text_view.font = FONT
    text_view.bg_color = BG_COLOR
    text_view.text_color = TEXT_COLOR
    text_view.text = func(var)
    return text_view

  def layout(self):
    self.header_view.size_to_fit()
    self.header_view.width = self.width
    self.binary_view.y = self.header_view.height


if __name__ == '__main__':
  SIMToolkitNegativeACK_path_str = '/System/Library/Audio/UISounds/SIMToolkitNegativeACK.caf'
  SIMToolkitNegativeACK_path = Path(SIMToolkitNegativeACK_path_str)
  
  hex_view = HexView(SIMToolkitNegativeACK_path)
  hex_view.present(style='panel', orientations=['portrait'])

