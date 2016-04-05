#!/usr/bin/env python
# coding=utf-8
import os
import argparse

print 'current dir ====> ', os.getcwd()
print '*' * 40

parser = argparse.ArgumentParser(
    description='A script for add script header message')
parser.add_argument('newfile')

args = parser.parse_args()

header_msg = {
    'py': '#!/usr/bin/env python\n#coding=utf-8\n',
    'c': '#include<stdio.h>\n'
}

if os.path.exists(os.getcwd()+'/'+args.newfile):
    print '\tfile already exists...'
else:
    if len(args.newfile.split('.')) == 2:
        newfile_type = args.newfile.split('.')[-1]

        if newfile_type in header_msg:
            f = open(args.newfile, 'w')
            print '\tadding header msg...'
            f.write(header_msg[newfile_type])
            f.close()
            msg = 'created %s' % args.newfile
            print msg.center(40, '*')
        else:
            temp = open(args.newfile, 'w')
            temp.close()
            print '\tcreated ', args.newfile
    else:
        temp = open(args.newfile, 'w')
        temp.close()
        print '\tcreated ', args.newfile
