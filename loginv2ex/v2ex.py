#!/usr/bin/env python
# coding:utf-8
import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
    'Origin': 'http://www.v2ex.com',
    'Referer': 'http://www.v2ex.com/signin',
    'Host': 'www.v2ex.com'
    }
sess = requests.Session()
LoginHtml = sess.get('http://www.v2ex.com/signin', headers=headers)
LoginSoup = BeautifulSoup(LoginHtml.text, 'lxml')
usrname = LoginSoup.find('input', {'class': 'sl'})['name']
usrpswd = LoginSoup.find('input', {'type': 'password'})['name']
once = LoginSoup.find('input', {'name': 'once'})['value']
from_data = {
    usrname: '3223340031@qq.com',
    usrpswd: 'usepython',
    'once': once,
    'next': '/'
    }
sess.post('http://www.v2ex.com/signin', from_data, headers=headers)

sethtml = sess.get('http://www.v2ex.com/settings', headers=headers)
soup = BeautifulSoup(sethtml.text, 'lxml')
email = soup.find('input', {'type': 'email'})['value']
print email
