#!/usr/bin/env python
# coding:utf-8
import requests, cookielib, re, time
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
    return jar

class Baidu(object):
    """贴吧签到"""

    url_sign = 'http://tieba.baidu.com/mo/m/sign?\
        tbs=79f03dacf896e9fc1466052875&fid=552164&kw='      # 签到url

    def __init__(self, cookies):
        self.cookies = cookies

    def get_token(self):
        """获取token参数"""
        url_of_token = 'https://passport.baidu.com/v2/api/?getapi&tpl=tb&apiver=v3'
        response = requests.get(url_of_token, cookies=self.cookies)
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
        url_login = 'https://passport.baidu.com/v2/api/?login'
        sess = requests.session()
        sess.post(url_login, data=form_data, cookies=cookie)
        usr_info = sess.get('http://tieba.baidu.com/f/user/json_userinfo').text
        if usr_info == 'null':
            print 'login failed..'
            exit(0)
        else:
            print 'login succeed!'
            return sess

    def sign_single_ba(self, sess, kw):
        """单个吧签到"""
        url = self.url_sign + kw
        html = sess.get(url).text
        soup = BeautifulSoup(html, 'html.parser')
        status = soup.select('body > div > span')[0].text
        return status

    def get_info(self, sess):
        """获取个人关注贴吧，以及各贴吧经验，等级并返回"""
        myFavor = 'http://tieba.baidu.com/mo/m?tn=bdFBW&tab=favorite'
        html = sess.get(myFavor).text
        soup = BeautifulSoup(html, 'html.parser')
        allLabel = soup.find_all('td')
        kws = [item.text.split('.')[-1] for item in allLabel[::3]]
        levels = [item.text for item in allLabel[1::3]]
        exercises = [item.text for item in allLabel[2::3]]
        return [kws, levels, exercises]

    def sign_all_ba(self, sess):
        """每个页的每个贴吧签到"""

        kws = self.get_info(sess)[0]
        for index, kw in enumerate(kws):
            try:
                status = self.sign_single_ba(sess, kw)
            except IndexError:
                status = u'签到异常.'
        temp = self.get_info(sess)
        levels = temp[1]
        print u'共{0}个吧'.format(len(levels))

def start(usrname, pswd):
    cookie = get_cookies()
    tieba = Baidu(cookie)
    token = tieba.get_token()
    res = tieba.login(token, usrname, pswd, cookie)
    tieba.sign_all_ba(res)

if __name__ == '__main__':
    usr = {
#        '*****': '*****',
#        '***': '****'
    }
    for usrname in usr:
        try:
            start(usrname, usr[usrname])
            print time.ctime(), '-', usrname, u'签到'
        except:
            print time.ctime(), '-', usrname, u'失败'

