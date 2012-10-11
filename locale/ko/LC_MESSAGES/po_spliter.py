#!/usr/bin/python
# encoding: utf-8
from glob import glob
import os
import sys
import re
from collections import OrderedDict


def main():
    target_file = None
    if len(sys.argv) < 2:
        print "need a file name for splitting."
        return 1
    else:
        try:
            target_file = open(sys.argv[1])
        except IOError:
            print "need a file name for spliting"
            return 1

    header = ''
    each_files = {}
    header_flag = False
    re_filepath = re.compile('^#:\s(.+):(\d+$)')
    while True:
        each_line = target_file.readline()
        if not each_line:
            break
        if header_flag == False and re_filepath.match(each_line) == None:
            header += each_line
            continue
        elif re_filepath.match(each_line):
            header_flag = True
            match_filepath = re_filepath.match(each_line)
            file_name = match_filepath.groups()[0]
            file_name = file_name.replace('../', '')
            file_line = match_filepath.groups()[1]
            if file_name not in each_files:
                each_files[file_name] = OrderedDict()
            each_files[file_name][file_line] = each_line
            while True:
                msg_line = target_file.readline()
                if msg_line in ['\n', '']:
                    each_files[file_name][file_line] += '\n'
                    break
                each_files[file_name][file_line] += msg_line

    target_file.close()

    for path, content in each_files.iteritems():
        for mkpath in os.path.dirname(path).split('/'):
            if not os.path.isdir(os.path.dirname(path)):
                os.mkdir(os.path.dirname(path))
        splited_file = open(path, 'w')
        for po_line in content.itervalues():
            splited_file.write(po_line)
        splited_file.close()

if __name__ == '__main__':
    main()
