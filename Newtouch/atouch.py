#!/usr/bin/env python
# coding:utf-8

import os
import argparse


header_msg = {
    'py': ("#!/usr/bin/env python\n"
           "# coding:utf-8\n"),
    'c': ("#include <stdio.h>\n\n"
          "int main (void)\n"
          "{\n    return 0;\n}\n"),
    'scm': ";;;\n",
    "html": "<!DOCTYPE HTML>",
    'm': '',
    'sh': "#!/bin/bash\n",
    'java': ''
}

class ArgsParser:
    """
    parser the command arguments
    """
    @staticmethod
    def args_parser():
        parser = argparse.ArgumentParser(
            description="""
            A simple script for add header message when create a new file.
            """
        )
        parser.add_argument('newfile')
        args = parser.parse_args()
        return args


class Atouch:
    """
    Usage egs:
        $ chmod +x atouch.py
        $ ./atouch.py -h
        $ ./atouch.py foo.py
        $ ./atouch.py bar.c
    """
    def is_file_exists(self, file_path):
        return True if os.path.exists(file_path) else False

    def write(self, newfile, model='w'):
        newfile_attrs = args.newfile.split('.') # newfile's file type
        with open(newfile, model) as nf:
            if newfile_attrs[-1] in header_msg:
                nf.write(header_msg[newfile_attrs[-1]])

    def main(self, args):
        file_path = os.path.join(os.path.dirname(__file__), args.newfile)
        if self.is_file_exists(file_path):
            print('\t{0} already exists...'.format(args.newfile))
        elif file_path.endswith("/"):
            print("No such directory")
        else:
            self.write(args.newfile)

if __name__ == '__main__':
    args = ArgsParser.args_parser()
    atouch = Atouch()
    atouch.main(args)
