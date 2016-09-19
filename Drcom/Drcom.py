#!/usr/bin/env python
# encoding: utf-8

import ConfigParser
import logging
import re

import requests


def log():
    logging.basicConfig(filename='drcom.log',
                        level=logging.DEBUG,
                        format='[%(levelname)s] [%(asctime)s',
                        datefmt='%d/%b/%y %H:%M:%S')
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(levelname)-6s[%(asctime)s]]: %(message)s')
    handler.setFormatter(formatter)
    logging.getLogger('').addHandler(handler)
    return logging

def read_config(config_path):
    configs = ConfigParser.ConfigParser()
    configs.read(config_path)
    count = configs.get('userinfo', 'count')
    password = configs.get('userinfo', 'enpassword')
    config_dict = {'count': count,
                   'password': password}
    return config_dict


class Drcom:

    LOG = log()
    host = "http://202.112.208.3/"
    headers = {
        "User-Agent": ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
                       "(KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36")
    }

    def __init__(self):
        self.configs = read_config('config.ini')
        self.count = self.configs.get('count')
        self.password = self.configs.get('password')
        self.session = requests.Session()
        self.session.headers = self.headers

    def http_requests(self, method, action, headers=None, form_data=None,
                      timeout=60):
        if method == "GET":
            res = self.sess.get(action, headers, timeout=timeout)
        elif method == "POST":
            res = self.sess.post(action, data=form_data, timeout=timeout)
        else:
            self.LOG.error("NOT FOUND METHOD {0}".format(method))
        return res
