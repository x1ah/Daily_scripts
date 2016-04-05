#!/usr/bin/env python
#coding=utf-8

import urllib
import re
import os

def GetHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

def GetVedio(html):
    mvpatt = r'hurl=(.+?\.jpg)'
    temp_patt = re.compile(mvpatt)
    get_list = re.findall(temp_patt, html)
    return get_list

def main(num):
    html = GetHtml('http://music.163.com/mv?id=%s' % num)
    vedio_list = GetVedio(html)
    vedioUrls = vedio_list[0].split("&")
    songer = vedioUrls[4].split('=')[1].decode('utf-8').strip().replace(' ', '-')
    song_name = vedioUrls[3].split('=')[1].decode('utf-8').strip().replace(' ', '-')
    store_filename = r'%s/%s.mp4' % (songer, song_name)
    # store_filename = store_filename_temp.replace(' ', '-')
    if os.path.exists(store_filename):
        print 'the MV already exists!'
    else:
        print 'Downloading The MV.....', store_filename
        os.mkdir(songer)
        urllib.urlretrieve(vedioUrls[0], store_filename)
        print 'Downloading completed....'

if __name__ == '__main__':
    num = raw_input('Input the MV num: ')
    main(num)
