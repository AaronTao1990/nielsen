import tablib
import xlrd
from optparse import OptionParser
import json

def read_file(filename):
    with open(filename, 'r') as f:
        return f.read()

def read_json_lines_file(filename):
    with open(filename, 'r') as f:
        lines = []
        for line in f.readlines():
            lines.append(line.strip('\n'))
        return '[' + ','.join(lines) + ']'

def export_to_excel(src_filename, tar_filename):
    dataset = tablib.Dataset()
    dataset.json = read_json_lines_file(src_filename)
    open(tar_filename, 'wb').write(dataset.xls)

def export_to_json(src_filename, tar_filename):
    wb = xlrd.open_workbook(src_filename)
    sh = wb.sheet_by_index(0)
    headers = sh.row_values(0)

    def gen_json_line(values):
        if len(headers) != len(values):
            raise Exception('invalid line : %s' % str(values))
        item = {}
        for i in range(len(headers)):
            item[headers[i]] = values[i]
        return json.dumps(item, ensure_ascii=False).encode('utf-8')

    items = []
    for rownum in range(sh.nrows-1):
        values = sh.row_values(rownum+1)
        item = gen_json_line(values)
        items.append(item)
    with open(tar_filename, 'wb') as f:
        for item in items:
            f.write(item + '\n')


def main(cmd, src_filename, tar_filename):
    if cmd == 'j2e':
        export_to_excel(src_filename, tar_filename)
    elif cmd == 'e2j':
        export_to_json(src_filename, tar_filename)
    else:
        pass

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-c', '--command', dest='cmd',
                      default='j2e',
                      help='command')
    parser.add_option('-s', '--src_filename', dest='src_filename',
                      default='src_filename.txt',
                      help='src filename')
    parser.add_option('-t', '--target_filename', dest='tar_filename',
                      default='tar_filename.txt',
                      help='tar filename')
    (options, args) = parser.parse_args()
    main(options.cmd, options.src_filename, options.tar_filename)
