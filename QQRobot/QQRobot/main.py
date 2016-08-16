#!/usr/bin/env python
# coding:utf-8

import logging
import time
from Login import Login
from PollMessage import Poll

def log():
    logging.basicConfig(filename='QQRobot.log',
                        level=logging.DEBUG,
                        format='[%(levelname)s] [%(asctime)s]: %(message)s',
                        datefmt='%d/%b/%Y %H:%M:%S')
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(levelname)-10s]: %(message)s')
    handler.setFormatter(formatter)
    logging.getLogger('').addHandler(handler)
    return logging

LOG = log()

def main():
    bot = Login()
    LOG.info('请扫描二维码.')
    print(bot.get_QRcode())
    Is_login = False
    while not Is_login:
        time.sleep(2)
        res = bot.is_login.split[','][-2]
        LOG.info(res)
        Is_login = True if '登录成功' in res else False
    LOG.info('获取ptwebqq...')
    bot.get_ptwebqq()
    LOG.info('获取vfwebqq...')
    bot.get_vfwebqq()
    LOG.info('获取psessionid...')
    bot.get_psessionid()

if __name__ == '__main__':
    main()

