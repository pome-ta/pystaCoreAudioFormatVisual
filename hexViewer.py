import os, ui, sys
from pathlib import Path

# https://github.com/humberry/hexviewer

# fixme: *.nes を取得
# fixme: offset そんなにいらない

FONT_SET = ('Ubuntu Mono', 11.5)
#SIMToolkitNegativeACK_path_str = '/System/Library/Audio/UISounds/SIMToolkitNegativeACK.caf'
#SIMToolkitNegativeACK_path = Path(SIMToolkitNegativeACK_path_str)

root_str = '/System/Library/Audio/UISounds/'
root_path = Path(root_str)

def get_dir(path=os.path.expanduser('~')):
  dirs = [] if path == os.path.expanduser('~') else ['..']
  files = []
  for entry in sorted(os.listdir(path)):
    if os.path.isdir(path + '/' + entry):
      dirs.append(entry)
    else:
      files.append(entry)
  dirs_and_files = ['/' + directory for directory in dirs]
  for file in files:
    if file[-4:] == '.caf':
      full_pathname = path + '/' + file
      size = '{} Bytes'.format(os.path.getsize(full_pathname))
      dirs_and_files.append('{:40} | {} '.format(file, size))
  return dirs_and_files


# バイナリ読み取り
def hex_view(filepath):
  return_value = ''
  try:
    with open(filepath, 'rb') as in_file:
      for line in range(0, os.path.getsize(filepath), 16):
        h = s = ''
        for c in in_file.read(16):
          i = get_ord(c)
          h += '{:02X}'.format(i) + ','
          # アルファベットと記号のみ抽出
          #s += chr(i) if 31 < i < 127 else '•'
          # 00 以外は 空白出力
          if 31 < i < 127:
            s += chr(i)
          elif 0 != i:
            s += ' '  # スペース喰うので
          else:
            s += '•'

        # 48 = 16(L)*16(R)*16(space)
        return_value += '{:04X}|{:48}|{:8}\n'.format(line, h, s)
  except Exception as e:
    return 'Error!\nFile = {}\nError = {}'.format(filepath, e)
  return return_value


def head_txt():
  mdl = ''
  end = ''
  for i in range(16):
    mdl += format(i, '02x') + ','
    end += format(i, 'x')

  top = 'ADRS|' + mdl + '|' + end + '\n'
  un_bar = '_' * 70 + '\n'
  return top + un_bar


def get_ord(c):
  if sys.version_info < (3, ):
    return ord(c)
  else:
    return c


class HexViewerView(ui.View):
  #pos = -1
  #searchstr = ''
  def __init__(self):
    #self.name = self.path = os.getcwd()
    self.name = self.path = root_str
    #self.bg_color = 'red' # todo: test
    self.tableview1 = self.make_tableview1()
    self.lst = self.make_lst()
    self.present('panel')

  def make_tableview1(self):
    tableview = ui.TableView()
    tableview.frame = self.frame
    tableview.x = tableview.y = 0
    tableview.flex = 'WH'
    tableview.row_height = 40
    tableview.bg_color = .128
    tableview.allows_selection = True
    self.add_subview(tableview)
    return tableview

  def make_lst(self):
    dirs_and_files = get_dir(self.path)
    lst = ui.ListDataSource(dirs_and_files)
    self.tableview1.data_source = lst
    self.tableview1.delegate = lst
    self.tableview1.editing = False
    lst.action = self.table_tapped
    lst.delete_enabled = False
    lst.font = FONT_SET
    lst.text_color = .872
    return lst

  def table_tapped(self, sender):
    rowtext = sender.items[sender.selected_row]
    filename_tapped = rowtext.partition('|')[0].strip()
    
    if filename_tapped[0] == '/':  # we have a directory
      if filename_tapped == '/..':  # move up one
        self.path = self.path.rpartition('/')[0]
      else:  # move down one
        self.path = self.path + filename_tapped
      self.name = self.path
      self.lst = self.make_lst()
      self.tableview1.reload()
    else:
      self.hexview_a_file(filename_tapped)
    

  def make_textview1(self):
    textview = ui.TextView()
    textview.bg_color = .128
    textview.editable = 0
    textview.name = 'tv_data'
    textview.frame = self.frame
    textview.width = self.width
    textview.height = self.height
    textview.x = self.width / 2 - textview.width / 2
    textview.y = 0

    textview.autoresizing = 'WHT'
    textview.font = FONT_SET
    textview.text_color = .872
    self.add_subview(textview)
    return textview

  def hexview_a_file(self, filename):
    self.tableview1.hidden = True
    self.textview1 = self.make_textview1()
    self.name = 'rom.nes :【 ' + filename + ' 】'
    full_pathname = self.path + '/' + filename
    bar = head_txt()
    self.textview1.text = bar + hex_view(full_pathname)


nes_view = HexViewerView()

