#!/usr/bin/env python
# coding:utf-8

import json
import random
import cookielib
import requests
from ShowQRcode import ShowQRcode

class Login:
    """
    Login SmartQQ
    """
    def __init__(self):
        self.headers = {
            "Accept-Encoding": "gzip, deflate, sdch, br",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Host": "ui.ptlogin2.qq.com",
            "Referer": "http://w.qq.com/",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
            )
        }
        self.session = requests.Session()
        # TODO: 暂不打算保存 Cookies,达到免扫码登录效果，之后再添加.

    def http_requests(self, method, url, headers, form_data=None, cookies=None, timeout=60):
        if method == "GET":
            response = self.session.get(url,
                                        headers=headers,
                                        cookies=cookies,
                                        timeout=timeout)
        elif method == "POST":
            response = self.session.post(url,
                                         headers=headers,
                                         cookies=cookies,
                                         data=form_data,
                                         timeout=timeout)
        else:
            print("NOT FOUND METHOD!")

        return [response.content, response.text]

    def get_QRcode(self):
        QRcode_url = ("https://ssl.ptlogin2.qq.com/ptqrshow?"
                      "appid=501004106&e=0&l=M&s=5&d=72&v=4&t={0}".format(random.random()))
        response = self.http_requests("GET", QRcode_url, self.headers)[0]
        with open('./QRcode.png', 'w') as PNG:
            PNG.write(response)
        return ShowQRcode('./QRcode.png').show()

    def save_cookies(self):
        cookies_file = 'cookies'
        jar = cookielib.LWPCookieJar(cookies_file)
        self.session.cookies = jar
        jar.save(ignore_expires=True,
                 ignore_discard=True)

    def is_login(self):
        url = ("https://ssl.ptlogin2.qq.com/ptqrlogin?webqq_type=10&"
               "remember_uin=1&login2qq=1&aid=501004106&u1=http%3A%2F"
               "%2Fw.qq.com%2Fproxy.html%3Flogin2qq%3D1%26webqq_type%"
               "3D10&ptredirect=0&ptlang=2052&daid=164&from_ui=1&pttype=1&"
               "dumy=&fp=loginerroralert&action=0-0-{0}&mibao_css=m_webqq&"
               "t=undefined&g=1&js_type=0&js_ver=10169&login_sig=&"
               "pt_randsalt=0".format(random.randint(2000, 1000000))
               )
        headers = self.headers
        headers['Referer'] = (
            "https://ui.ptlogin2.qq.com/cgi-bin/login?daid=164&target=self&"
            "style=16&mibao_css=m_webqq&appid=501004106&enable_qlogin=0&"
            "no_verifyimg=1&s_url=http%3A%2F%2Fw.qq.com%2Fproxy.html&"
            "f_url=loginerroralert&strong_login=1&login_state=10&t=20131024001"
        )
        response = self.http_requests("GET", url, headers)[0]
#        self.save_cookies()
        return response.split(',')[4]
#        return True if '登录成功' in response else False

    def get_ptwebqq(self):
        self.ptwebqq = self.session.cookies['ptwebqq']
        self.uin = self.session.cookies['uin']
        return self.ptwebqq

    def get_vfwebqq_and_psessionid(self):
        headers = self.headers
        get_url = 'http://d1.web2.qq.com/channel/login2'
        headers.update({
            'Accept-Encoding': 'gzip, deflate',
            'Origin': 'http://d1.web2.qq.com',
            'Referer': 'http://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'd1.web2.qq.com'
        })
        form_data = {
            'r': json.dumps({
                "ptwebqq": self.ptwebqq,
                "clientid": 53999199,
                "psessionid": "",
                "status": "online"
            })
        }
        print headers, form_data
        res = self.http_requests('POST', get_url, headers, cookies=self.session.cookies, form_data=form_data)
#        res_dict = json.loads(str(res))
#        self.psessionid = res_dict['result']['psessionid']
#        self.vfwebqq = res_dict['result']['vfwebqq']
        return res

