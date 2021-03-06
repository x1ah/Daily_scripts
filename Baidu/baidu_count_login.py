#!/usr/bin/env python
# coding:utf-8
try:
    import cookielib
except:
    import http.cookiejar as cookielib

import re
import requests
from prettytable import PrettyTable
from bs4 import BeautifulSoup


def get_cookies():
    """获取百度 cookies, 并写入文件."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
            "(KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36"
        )
    }
    save_cookies_file = 'cookies.txt'
    jar = cookielib.LWPCookieJar(save_cookies_file)
    sess = requests.session()
    sess.headers = headers
    sess.cookies = jar
    sess.get('http://tieba.baidu.com/')
    jar.save(ignore_expires=True, ignore_discard=True)
    return jar


class Baidu(object):
    """贴吧签到"""

    sign_url = (
        "http://tieba.baidu.com/mo/m/sign?"
        "tbs=79f03dacf896e9fc1466052875&fid=552164&kw="
    )       # 签到url

    def __init__(self, cookies):
        self.sess = requests.Session()
        self.sess.headers = {"Cookie": cookies}

    def get_token(self):
        """获取token参数"""
        url_to_token = 'https://passport.baidu.com/v2/api/?getapi&tpl=tb&apiver=v3'
        response = self.sess.get(url_to_token)
        json = response.text
        token = re.findall('token\" : "(\w+)\",', json)[0]
        return token

    def login(self, token, usrname, pswd, cookie):
        """登录并返回状态"""
        form_data = {
            "token": token,
            "tpl": 'tb',
            "loginmerge": "true",       # 必要必要必要参数！！！！
            "username": usrname,
            "password": pswd
        }
        login_url = 'https://passport.baidu.com/v2/api/?login'
        sess = requests.session()
        sess.post(login_url, data=form_data, cookies=cookie)
        usr_info = sess.get('http://tieba.baidu.com/f/user/json_userinfo').text
        if usr_info == 'null':
            print('登录失败！')
            exit(0)
        else:
            print('登录成功!')
            return sess

    def sign_single_ba(self, kw):
        """单个吧签到"""
        url = self.sign_url + kw
        html = self.sess.get(url, timeout=30).text
        soup = BeautifulSoup(html, 'html.parser')
        status = soup.select('body > div > span')[0].text
        return status

    def get_info(self, sess):
        """获取个人关注贴吧，以及各贴吧经验，等级并返回"""
        myFavor = 'http://tieba.baidu.com/mo/m?tn=bdFBW&tab=favorite'
        html = self.sess.get(myFavor).text
        soup = BeautifulSoup(html, 'html.parser')
        allLabel = soup.find_all('td')
        kws = [item.text.split('.')[-1] for
               item in allLabel[::3]]
        levels = [item.text for item in allLabel[1::3]]
        exercises = [item.text for item in allLabel[2::3]]
        return [kws, levels, exercises]

    def sign_all_ba(self):
        """每个页的每个贴吧签到"""
        table = PrettyTable([u'贴吧', u'签到状态'])
        table.padding_width = 2

        kws = self.get_info(self.sess)[0]
        for index, kw in enumerate(kws):
            try:
                status = self.sign_single_ba(kw)
            except IndexError:
                status = u'签到异常.'
            print(u'{0} {1}'.format(kw, status))
            table.add_row([kw, status])
        temp = self.get_info(self.sess)
        levels = temp[1]
        exercises = temp[2]
        table.add_column(u'经验', exercises)
        table.add_column(u'等级', levels)
        print(table)
        print(u'共{0}个吧'.format(len(levels)))


def start(usrname, pswd):
#    cookie = get_cookies()
    cookie = open("cookies", 'r').read()
    tieba = Baidu(cookie)
#    token = tieba.get_token()
#    res = tieba.login(token, usrname, pswd, cookie)
    tieba.sign_all_ba()

if __name__ == '__main__':
#    try:
#        usrname = raw_input('手机/邮箱/用户名: ')
#        pswd = raw_input('密码: ')
#    except:
#        usrname = input('手机/邮箱/用户名: ')
#        pswd = input('密码: ')

    start(1, 0)
