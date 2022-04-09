from pathlib import Path
import ui

# https://github.com/humberry/hexviewer

FONT = ('Ubuntu Mono', 11.5)
BG_COLOR = .128
TEXT_COLOR = .872
HEX_RANGE = range(16)


def set_header_str():
  addr_txt = ','.join([format(a, '02X') for a in HEX_RANGE])
  hex_txt = ''.join([format(h, 'X') for h in HEX_RANGE])
  return f'ADRS| {addr_txt}|{hex_txt}'


class HexView(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.bg_color = 'slategray'
    self.header_view = self.setup_header()
    self.main_view = self.setup_hextext()
    self.add_subview(self.header_view)
    self.add_subview(self.main_view)

  def setup_hextext(self):
    # xxx: ぶっこむ関数変えればいいだけでは？
    hextext = ui.TextView()
    hextext.editable = False
    hextext.font = FONT
    hextext.bg_color = 'maroon'#BG_COLOR
    hextext.text_color = TEXT_COLOR
    hextext.flex = 'WH'
    #hextext.size_to_fit()
    dummytext = ''
    for n in range(100):
      dummytext += set_header_str() + '\n'
    hextext.text = dummytext
    return hextext
    
  
  def setup_header(self):
    header = ui.TextView()
    header.editable = False
    header.font = FONT
    header.bg_color = BG_COLOR
    header.text_color = TEXT_COLOR
    header.flex = 'W'
    header.size_to_fit()
    header.text = set_header_str()
    return header

  def layout(self):
    self.header_view.width = self.width
    #self.main_view.width = self.width
    self.main_view.y = self.header_view.height


if __name__ == '__main__':
  hex_view = HexView()
  hex_view.present(style='panel', orientations=['portrait'])

