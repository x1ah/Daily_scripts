# !/usr/bin/python
# coding: utf-8

import os

import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable


quit = lambda : exit(0)
clear = lambda: os.system("clear")

def Soup(session, url, **args):
    html = session.get(url, **args)
    soup = BeautifulSoup(html.text, 'lxml')
    return soup


class HTTPRequest:

    session = requests.session()
    session.headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.86 Safari/537.36"
    }


    def get(self, url, **args):
        return self.session.get(url, **args)

    def post(self, url, **args):
        return self.session.post(url, **args)

def table_print(title, conts, display=True):
    table = PrettyTable(title)
    table.padding_width = 2
    if isinstance(conts[0], list):
        [table.add_row(cont) for cont in conts]
    else:
        table.add_row(conts)
    if display:
        print(table)

def validate_login(content, validator, default):
    """
    content: 检查文本
    所有判断条件在validator字典传入，validator对应键值为:
    {
        文本内(content)所含的字符串: [状态, 返回信息]
    }
    return: 登录状态
    """

    for condition in validator.keys():
        if condition in content:
            return validator.get(condition)
    return default

def rinput(message):
    try:
        res = raw_input(message)
    except:
        res = input(message)
    return res
