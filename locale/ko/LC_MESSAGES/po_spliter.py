#!/usr/bin/python
# encoding: utf-8
from glob import glob
import os
import sys
import re
from collections import OrderedDict
import pdb

def main(target_file):

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

    for path, content in each_files.iteritems():
        path = 'splited/' + path
        path_list = []
        for mkpath in os.path.dirname(path).split('/'):
            path_list.append(mkpath)
            joined_path_list = '/'.join(path_list)
            repr(joined_path_list)
            if not os.path.isdir(joined_path_list) and joined_path_list.strip() != '':
                print joined_path_list
                os.mkdir(joined_path_list)
        splited_file = open(path, 'w')
        splited_file.write(header)
        for po_line in content.itervalues():
            splited_file.write(po_line)
        splited_file.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "need a file name for splitting."
    else:
        try:
            file_list = sys.argv[1:]
            
            for target_file in file_list:
                target_file = open(target_file)
                main(target_file)
                target_file.close()
            
        except IOError:
            print "need a file name for spliting"
