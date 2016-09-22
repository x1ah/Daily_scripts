#!/usr/bin/env python
# encoding: utf-8

import argparse
import ConfigParser
import logging
import re
import os
import sys

import requests


def log():
    logging.basicConfig(filename='drcom.log',
                        level=logging.DEBUG,
                        format='[%(levelname)s] [%(asctime)s]: %(message)s',
                        datefmt='%d/%b/%y %H:%M:%S')
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(levelname)-6s[%(asctime)s]] %(message)s')
    handler.setFormatter(formatter)
    logging.getLogger('').addHandler(handler)
    return logging

def read_config(config_path):
    configs = ConfigParser.ConfigParser()
    configs.read(config_path)
    count = configs.get('userinfo', 'count')
    enpassword = configs.get('userinfo', 'enpassword')
    config_dict = {'count': count,
                   'enpassword': enpassword}
    return config_dict

def get_sys_version():
    return sys.platform

class ParseArgs:
    def pargs(self):
        parser = argparse.ArgumentParser(
            description="student's count and password.")
        parser.add_argument('count')
        parser.add_argument('password')
        self.args = parser.parse_args()
        print self.args.count
        return {'count': self.args.count,
                'password': self.args.password}

    def __str__(self):
        return self.args

    __repr__ = __str__

class Drcom:

    LOG = log()
    host = "http://202.112.208.3/"
    is_login = False
    headers = {
        "User-Agent": ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
                       "(KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36")
    }

    def __init__(self):
        self.configs = read_config('config.ini')
        self.count = self.configs.get('count')
        self.enpassword = self.configs.get('enpassword')
        self.sess = requests.Session()
        self.sess.headers = self.headers
        self.post_data = {
            "DDDDD": self.count,
            "upass": self.enpassword,
            "R1": "0",
            "R2": "1",
            "para": "00",
            "0MKKey": "123456"
        }


    def http_requests(self, method, action, headers=None, form_data=None,
                      timeout=60):
        if method == "GET":
            res = self.sess.get(action, timeout=timeout)
        elif method == "POST":
            res = self.sess.post(action, data=form_data, timeout=timeout)
        else:
            self.LOG.error("NOT FOUND METHOD {0}".format(method))
        return res


    def calc_flow(self, flow):
        flow0 = flow % 1024
        flow1 = flow - flow0
        flow0 = flow0 * 1000
        flow0 = flow0 - flow0 % 1024
        return float('{0}.{1}'.format(flow1 / 1024, flow0 / 1024))

    def get_user_message(self):
        if self.is_login:
            message_html = self.http_requests("GET", self.host).content
            flow = int(re.findall("flow=\'(\d+)", message_html)[0])
            used = self.calc_flow(flow)
            balance = 25000 - used
            self.used , self.balance = used, balance

    def login(self):
        if not self.is_login:
            res = self.http_requests("POST", self.host, form_data=self.post_data).content
            self.is_login = 'successfully' in res
            self.get_user_message() if self.is_login else None
            return self.is_login
        else:
            self.LOG.error("YOU ARE ALDEARY LOGIN.")

    def logout(self):
        if self.is_login():
            res = self.http_requests("GET", self.host+"F.htm").content
            self.is_login = "can not modify" in res
            return self.is_login
        else:
            self.LOG.error("YOU ARE NOT LOGIN.")


def start():
    try:
        print 'try.....'
        main = Drcom()
        main.login()
        main.LOG.info('Used {0} MBytes, {1} MBytes balanced'.format(main.used, main.balance))
    except ConfigParser.NoSectionError:
        print 'except.....'
        config_parser = ParseArgs().pargs()
        count, password = config_parser.get('count'), config_parser.get('password')
        os.system("./encrypt {0} {1}".format(count, password))
        main = Drcom()
        main.login()
        main.LOG.info('Used {0} MBytes, {1} MBytes balanced'.format(main.used, main.balance))

if __name__ == "__main__":
    start()
#    main = Drcom()
#    main.login()
#    main.LOG.info('Used {0} MBytes, {1} MBytes balanced'.format(main.used, main.balance))
#    main.logout()
