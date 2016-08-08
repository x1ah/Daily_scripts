#!/usr/bin/env python
# coding:utf-8
import os
import argparse


header_msg = {
    'py': '#!/usr/bin/env python\n# coding:utf-8\n',
    'c': '#include <stdio.h>\n',
    'scm': ';;;\n',
    'm': ''
}


def par():
    parser = argparse.ArgumentParser(
        description='A script for add script header message'
    )
    parser.add_argument('newfile')
    args = parser.parse_args()
    return args


def file_exists(file_path):
    return True if os.path.exists(file_path) else False


def main(args):
    file_path = os.getcwd() + '/' + args.newfile
    if file_exists(file_path):
        print('\t{0} already exists...'.format(args.newfile))
    else:
        newfile_attrs = args.newfile.split('.')
        with open(args.newfile, 'w') as f:
            if (len(newfile_attrs) == 2) and (newfile_attrs[-1] in header_msg):
                f.write(header_msg[newfile_attrs[-1]])

if __name__ == '__main__':
    args = par()
    main(args)
