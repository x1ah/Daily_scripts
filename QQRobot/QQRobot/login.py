#!/usr/bin/env python
# coding:utf-8

import requests
from bs4 import BeautifulSoup
#from ShowQRcode import ShowQRcode

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

    def http_requests(self, method, url, form_data=None, timeout=60):
        if method == "GET":
            response = self.session.get(url,
                                       headers=self.headers,
                                       timeout=timeout)
        elif method == "POST":
            response = self.session.post(url,
                                        headers=self.headers,
                                        form_data=form_data,
                                        timeout=timeout)
        else:
            print("NOT FOUND METHOD!")

        return [response.content, response.text]

    def get_QRcode(self):
        QRcode_url = 'https://ssl.ptlogin2.qq.com/ptqrshow'
        response = self.http_requests("GET", QRcode_url)[0]
        with open('./QRcode.png', 'w') as PNG:
            PNG.write(response)

