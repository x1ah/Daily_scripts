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
#    password = configs.get('userinfo', 'password')
#    host = configs.get('userinfo', 'host')
    config_dict = {'count': count}
    return config_dict

def conf(config_path):
    configs = ConfigParser.ConfigParser()
    configs.read(config_path)
    return configs

class Drcom:

    LOG = log()
    en_pswd = conf('ENPSWD.ini')
    configs = read_config('config.ini')
    count = configs.get('count')
    password = en_pswd.get('enpswd', 'enpswd')
#    host = configs.get('host')

    def login(self):
        url = 'http://202.112.208.3/'
        data_form = {
            "DDDDD": self.count,
            "upass": self.password,
            "R1": '0',
            "R2": '1',
            "para": "00",
            "0MKKey": "123456"
        }
        res = requests.post(url, data=data_form)
        print res.content
        return res
