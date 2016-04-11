#!/usr/bin/env python
#coding=utf-8

import urllib
import re
import os

def gethtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

def getvedio(html):
    mvpatt = r'hurl=(.+?\.jpg)'
    temp_patt = re.compile(mvpatt)
    get_list = re.findall(temp_patt, html)
    return get_list


def callbackfunc(already, a_ll, remote):
    persent = 100.0 * already * a_ll / remote
    if persent > 100:
        persent = 100
    print '%.2f%%\r' % persent, '已经下载： ', a*b, '文件大小: ', c

def main(num):
    html = gethtml('http://music.163.com/mv?id=%s' % num)
    vedio_list = getvedio(html)
    vedioUrls = vedio_list[0].split("&")
    songer = vedioUrls[4].split('=')[1].decode('utf-8').strip().replace(' ', '-')
    song_name = vedioUrls[3].split('=')[1].decode('utf-8').strip().replace(' ', '-')
    store_filename = r'%s/%s.mp4' % (songer, song_name)
    # store_filename = store_filename_temp.replace(' ', '-')
    if os.path.exists(store_filename):
        print 'the MV already exists!'
    else:
        os.mkdir('%s/' % songer)
        print 'Downloading The MV.....', store_filename
        #os.mkdir(songer)
        urllib.urlretrieve(vedioUrls[0], store_filename, callbackfunc)
        print 'Downloading completed....'

if __name__ == '__main__':
    num = raw_input('Input the MV num: ')
    main(num)
