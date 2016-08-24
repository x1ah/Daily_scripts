#!/usr/bin/env python
# coding:utf-8

import json
import cookielib
import requests
from ShowQRcode import ShowQRcode


class Login:
    """
    Login SmartQQ
    """
    def __init__(self):
        self.headers = {
            "Referer": "http://w.qq.com/",
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
            )
        }
        self.session = requests.Session()
        self.session.headers = self.headers
        # TODO: 暂不打算保存 Cookies,达到免扫码登录效果，之后再添加.

    def http_requests(self, method, url, form_data=None, timeout=30):
        if method == "GET":
            response = self.session.get(url,
                                        timeout=timeout)
        elif method == "POST":
            response = self.session.post(url,
                                         data=form_data,
                                         timeout=timeout)
        else:
            print("NOT FOUND METHOD!")

        return [response.content, response.text]

    def get_QRcode(self):
        QRcode_url = ("https://ssl.ptlogin2.qq.com/ptqrshow?"
                      "appid=501004106&e=0&l=M&s=5&d=72&v=4&t=0.1")
        response = self.http_requests("GET", QRcode_url)[0]
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
               "dumy=&fp=loginerroralert&action=0-0-157510&mibao_css=m_webqq&"
               "t=1&g=1&js_type=0&js_ver=10169&login_sig=&"
               "pt_randsalt=0")
        self.session.headers['Referer'] = (
            "https://ui.ptlogin2.qq.com/cgi-bin/login?daid=164&target=self&"
            "style=16&mibao_css=m_webqq&appid=501004106&enable_qlogin=0&"
            "no_verifyimg=1&s_url=http%3A%2F%2Fw.qq.com%2Fproxy.html&"
            "f_url=loginerroralert&strong_login=1&login_state=10&t=20131024001"
        )
        response = self.http_requests("GET", url, self.session.headers)[0]
        self.Ptwebqq_url = response.split("','")[2]
#        self.save_cookies()
        return response
#        return True if '登录成功' in response else False

    def get_ptwebqq(self):
        self.http_requests("GET", self.Ptwebqq_url, timeout=60)
        self.ptwebqq = self.session.cookies['ptwebqq']
        return self.ptwebqq

    def get_vfwebqq(self):
        vfwebqq_url = ("http://s.web2.qq.com/api/getvfwebqq?"
                       "ptwebqq={0}&clientid=53999199&psessionid=&"
                       "t=0.1".format(self.ptwebqq))
        self.session.headers['Referer'] = 'http://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1'
        self.session.headers['Origin'] = 'http://s.web2.qq.com'
        vfw_res = self.http_requests('GET', vfwebqq_url, timeout=60)
        self.vfwebqq = json.loads(vfw_res[0])['result']['vfwebqq']
        return self.vfwebqq

    def get_psessionid(self):
        api_url = 'http://d1.web2.qq.com/channel/login2'
        self.session.headers.update({'Host': 'd1.web2.qq.com',
                                     "Origin": "http://d1.web2.qq.com",
                                     "Referer": (
                                         "http://d1.web2.qq.com/proxy.html?"
                                         "v=20151105001&callback=1&id=2")})
        form_data = {'r': json.dumps({"ptwebqq": self.ptwebqq,
                                      "clientid": 53999199,
                                      "psessionid": '',
                                      "status": "online"})}
        pse_res = self.http_requests("POST", api_url, form_data=form_data)
        result = json.loads(pse_res[0])['result']
        self.psessionid, self.uin = result['psessionid'], result['uin']
        return self.psessionid

    def poll(self):
        poll_url = 'http://d1.web2.qq.com/channel/poll2'
        form_data ={'r': json.dumps({"ptwebqq": self.ptwebqq,
                                     "clientid": 53999199,
                                     "psessionid": self.psessionid,
                                     "key": ''})}
        poll_res = self.http_requests("POST", poll_url, form_data=form_data)
        return 'poll error' if 'errmsg' in poll_res else poll_res

    def send_msg(self, msg, to_id, msg_type):
        if msg_type == 'message':
            post_url = 'http://d1.web2.qq.com/channel/send_buddy_msg2'
            form_data = {'r': json.dumps({'to': to_id,
                                          "content": json.dumps(
                                              [msg,
                                               ["font",
                                                {"name": "宋体",
                                                 "size": 10,
                                                 "style": [0, 0, 0],
                                                 "color": "000000"}]]),
                                          "face": 729,
                                          "clientid": 53999199,
                                          "msg_id": 34220099,
                                          "psessionid": self.psessionid,
                                          })}
            send_res = self.http_requests("POST", post_url, form_data=form_data)
            return send_res
        else:
            return 'No Action.'
