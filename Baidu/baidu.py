#!/usr/bin/env python
# coding:utf-8
import requests, cookielib, re
from prettytable import PrettyTable
from time import sleep
from bs4 import BeautifulSoup

headers = {
    "Accept-Encoding": "gzip, deflate, br",
    "Accept - Language": "zh - CN, zh;q = 0.8",
    "Content-Type": "application/x-www-form-urlencoded",
    'Host': 'passport.baidu.com',
    'Origin': "http://tieba.baidu.com",
    "Referer": "http://tieba.baidu.com/",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent":
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36\
    (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36",
}

def getcookies():
    '''获取百度 cookies, 并写入文件.'''
    cookiefile = 'cookies.txt'
    jar = cookielib.LWPCookieJar(cookiefile)
    sess = requests.session()
    sess.headers = headers
    sess.cookies = jar
    sess.get('http://www.baidu.com/')
    jar.save(ignore_expires=True, ignore_discard=True)
    return jar

class baidu(object):


    simple_headers = {
        "User-Agent":
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36\
        (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36"
        }

    markUrl = 'http://tieba.baidu.com/mo/m/sign?\
        tbs=79f03dacf896e9fc1466052875&fid=552164&kw='      # 签到url

    def __init__(self, cookies):
        self.cookies = cookies

    def get_token(self):
        '''获取token参数'''
        tokenUrl = 'https://passport.baidu.com/v2/api/?getapi&tpl=tb&apiver=v3'
        response = requests.get(tokenUrl, headers=self.simple_headers,
                                cookies=self.cookies)
        json = response.text
        token = re.findall('token\" : "(\w+)\",', json)[0]
        return token

    def login(self, token, usrname, pswd, cookie):
        '''登录并返回状态'''
        form_data = {
            "token": token,
            "tpl": 'tb',
            "loginmerge": "true",       # 必要必要必要参数！！！！
            "username": usrname,
            "password": pswd
        }
        loginUrl = 'https://passport.baidu.com/v2/api/?login'
        sess = requests.session()
        sess.headers = self.simple_headers
        sess.post(loginUrl, data=form_data, cookies=cookie)
        usrInfo = sess.get('http://tieba.baidu.com/f/user/json_userinfo').text
        if usrInfo == 'null':
            print '登录失败！'
            exit(0)
        else:
            print '登录成功!'
            return sess


        myFavor= 'http://tieba.baidu.com/mo/m?tn=bdFBW&tab=favorite'


    def markSingle(self, sess, kw):#, cookie):
        '''单个吧签到'''
#        markUrl = 'http://tieba.baidu.com/sign/add'
        url = self.markUrl + kw
        html = sess.get(url).text
        soup = BeautifulSoup(html, 'html.parser')
        status = soup.select('body > div > span')[0].text
#        tbs = re.search('tbs\': "(\w+)\"', html).group(1)
#        kw = re.search('name=\"kw\" value=\"(.+)\" ', html).group(1)
#        form_data = {
#            "ie": "utf-8",
#            "kw": kw,
#            "tbs": tbs
#        }
#        r = sess.post(markUrl, data=form_data, cookies=cookie)
#        json = r.json()         # 获取返回json
#        status = json[u'error']
#        res = u'签到成功' if len(status) == 0 else status
        res = status
#        print res
        return res
#        return [kw, res]

    def markAllLikes(self, sess, cookie):
        '''每个页的每个贴吧签到'''
#        likeUrl = 'http://tieba.baidu.com/f/like/mylike'
        table = PrettyTable(['贴吧', '签到状态', '经验', '等级'])
        table.padding_width = 2

        myFavor = 'http://tieba.baidu.com/mo/m?tn=bdFBW&tab=favorite'
        html = sess.get(myFavor).text#, cookies=cookie)
        soup = BeautifulSoup(html, 'html.parser')
        allLabel = soup.find_all('td')
        kws = [item.text.split('.')[-1] for item in allLabel[::3]]
        levels = [item.text for item in allLabel[1::3]]
        exercises = [item.text for item in allLabel[2::3]]
#        print len(kw), len(level), len(exercise)
        for index, kw in enumerate(kws):
            status = self.markSingle(sess, kw)
            print kw, ' ', status
            table.add_row([kw, status, exercises[index], levels[index]])
        print table
#            print j, level[i], exercise[i]

#        totalPages = int(re.findall('pn=(\d+)\"', html.text)[-1])
#
#        for page in range(1, totalPages + 1):
#            pageUrl = 'http://tieba.baidu.com/f/like/mylike?&pn=' + str(page)
#            singlePageHtml = sess.get(pageUrl, cookies=cookie)
#            bs = BeautifulSoup(singlePageHtml.text, 'html.parser')
#            urls = [url['href'] for url in bs.select('tr > td:nth-of-type(1) > a')]
#            allUrls = map(lambda x: 'http://tieba.baidu.com' + x, urls)
#            exercise = [exe.text for exe in bs.select('tr > td:nth-of-type(2) > a')]
#            level = [le.text for le in
#                      bs.select('tr > td:nth-of-type(3) > a > div:nth-of-type(2)')]
#            for index, single in enumerate(allUrls):
##                sleep(5)
#                status = self.markSingle(sess, single, cookie)
#                status.append(exercise[index])
#                status.append(level[index])
#                table.add_row(status)
#                print status[0], status[1]
##            sleep(60)
#        print table

if __name__ == '__main__':
    usrname = '15279473578'#15650700313'#raw_input('用户名: ')
    pswd = 'my2085145'#199666tb'#raw_input('密码: ')
    cookie = getcookies()
    tieba = baidu(cookie)
    token = tieba.get_token()
    tieba = baidu(cookie)
    res = tieba.login(token, usrname, pswd, cookie)
#    tieba.markSingle(res, '情感')
    tieba.markAllLikes(res, cookie)
