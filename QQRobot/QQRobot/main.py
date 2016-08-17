#!/usr/bin/env python
# coding:utf-8

import logging
import sys
import time
import json
from Login import Login


def log():
    logging.basicConfig(filename='QQRobot.log',
                        level=logging.DEBUG,
                        format='[%(levelname)s] [%(asctime)s]: %(message)s',
                        datefmt='%d/%b/%Y %H:%M:%S')
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(levelname)-6s[%(asctime)s]]: %(message)s')
    handler.setFormatter(formatter)
    logging.getLogger('').addHandler(handler)
    return logging

LOG = log()


def hand_msg(msg):
    if 'error' in msg:
        return 'None New Message'
    msg_dict = json.loads(msg)
    msg_content = msg_dict['result'][0]['value']['content'][-1]
    from_uin = msg_dict['result'][0]['value']['from_uin']
    msg_type = msg_dict['result'][0]['poll_type']
    return [msg_content, from_uin, msg_type]


def main():
    send_msg = '您好,这里是机器人,稍后回复您的消息,抱歉.(望勿频繁调戏机器人...)'
    bot = Login()
    LOG.info('请扫描二维码.')
    print(bot.get_QRcode())
    Is_login = False
    while not Is_login:
        time.sleep(2)
        res = bot.is_login().split(',')[-2]
        LOG.info(res)
        Is_login = True if '登录成功' in res else False
    LOG.info('获取ptwebqq...')
    bot.get_ptwebqq()
    LOG.info('获取vfwebqq...')
    bot.get_vfwebqq()
    LOG.info('获取psessionid...')
    bot.get_psessionid()
    LOG.info('等待消息...')
    STOP = False
    while not STOP:
        time.sleep(1)
        try:
            msg = bot.poll()
            msg_content, from_uin, msg_type = hand_msg(msg[0])
            LOG.info('{0} 发来一条消息: {1}'.format(from_uin, msg_content.encode('utf-8')))
            send_status = bot.send_msg(send_msg, from_uin, msg_type)
            LOG.info('回复 {0}: {1}'.format(from_uin, send_status))
        except KeyboardInterrupt:
            LOG.info('See You...')
            STOP = True
        except:
            LOG.error(sys.exc_info())

if __name__ == '__main__':
    main()
