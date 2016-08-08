#!/usr/bin/env python
# coding:utf-8

import os
import re
import requests
import argparse


class ParseArgs:
    '''parser command line args'''
    def __init__(self):
        pass

    def mv_id(self):
        _parser = argparse.ArgumentParser(
            description='Download cloud music MV'
        )
        _parser.add_argument('mv_id')
        self.args = _parser.parse_args()
        return self.args.mv_id

    def __str__(self):
        return self.args.mv_id

    __repr__ = __str__


class DownloadMV(object):
    def __init__(self, mv_id):
        self.mv_id = mv_id

    def mv_url(self):
        html = requests.get(
            'http://music.163.com/mv?id={0}'.format(self.mv_id)
        ).text
        self.mv_url = re.findall('murl=(.+\.mp4)', html)[0]
        return self.mv_url

    def download(self):
        '''
        first method....
        also can urllib.urlretrieve
        '''
        os.system('wget {0}'.format(self.mv_url))


def start():
    parser = ParseArgs()
    mv_id = parser.mv_id()
    main = DownloadMV(mv_id)
    main.download()


if __name__ == '__main__':
    start()
