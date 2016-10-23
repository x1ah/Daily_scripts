#!/usr/bin/env python
# encoding: utf-8

import os
import re
import sys
import time
import sqlite3
import contextlib
import ConfigParser
import logging

#from logging import (getLogger, StreamHandler,
#    Formatter, getLoggerClass, INFO, DEBUG)

import requests

@contextlib.contextmanager
def ignored(*exceptions):
    try:
        yield
    except:
        pass

def create_logger():
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter('[%(asctime)s]: %(message)s'))
    logger = logging.getLogger('')
    logger.addHandler(handler)
    return logger

def read_config(config_path):
    """Read user config from config_path"""
    configs = ConfigParser.ConfigParser()
    configs.read(config_path)
    count = configs.get('userinfo', 'count')
    password = configs.get('userinfo', 'password')
    enpassword = configs.get('userinfo', 'enpassword')
    config_dict = {'count': count,
                   'password': password,
                   'enpassword': enpassword}
    return config_dict


sys_version = lambda: sys.platform


class Drcom:

    LOG = create_logger()
    host = "http://202.112.208.3/"
    IS_LOGIN = False
    headers = {
        "User-Agent": ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
                       "(KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36")
    }

    def __init__(self):
        self.configs = read_config('config.ini')
        self.count = self.configs.get('count')
        self.password = self.configs.get('password')
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
            res = self.sess.get(action)
        elif method == "POST":
            res = self.sess.post(action, data=form_data)
        else:
            self.LOG.error("NOT FOUND METHOD {0}".format(method))
        return res

    def get_user_message(self):
        """get user message such as used flow, balance"""
        if self.IS_LOGIN:
            message_html = self.http_requests("GET", self.host).content
            flow = int(re.findall("flow=\'(\d+)", message_html)[0])
            used = self.calc_flow(flow)
            self.used , self.balance = used, 25600 - used
            return True

    def login(self):
        if not self.IS_LOGIN:
            res = self.http_requests("POST",
                                     self.host,
                                     form_data=self.post_data).content
            self.IS_LOGIN = 'You have successfully logged into our system' in res
            self.get_user_message() if self.IS_LOGIN else None
        else:
            self.LOG.error("YOU ARE ALDEARY LOGIN.")
        return self.IS_LOGIN

    def calc_flow(self, flow):
        flow0 = flow % 1024
        flow1 = flow - flow0
        flow0 = flow0 * 1000
        flow0 = flow0 - flow0 % 1024
        return float('{0}.{1}'.format(flow1 / 1024, flow0 / 1024))

    def logout(self):
        if self.IS_LOGIN():
            res = self.http_requests("GET", self.host+"F.htm").content
            self.IS_LOGIN = "can not modify" in res
            return self.IS_LOGIN
        else:
            self.LOG.error("YOU ARE NOT LOGIN.")


class DB:
    def __init__(self, db):
        self.db = db
        self.connect = sqlite3.connect(self.db)
        self.cursor = self.connect.cursor()

    def select(self, SQL, *args):
        """
        eg:
        >>> DB.select('SELECT * FROM CUMTB WHERE Sno=?;', "12345")
        """
        self.cursor.execute(SQL, args)
        return self.cursor.fetchall()

    def delete(self, SQL, *args):
        """
        eg:
        >>> DB.delete('delete FROM CUMTB WHERE Sno=?;', "12423")
        """
        self.cursor.execute(SQL, args)
        self.connect.commit()

    def insert(self, SQL, *args):
        """
        eg:
        >>> DB.insert('insert into CUMTB values {};', ('123145', '23456'))
        """
        s = SQL.format(args)
        self.cursor.execute(s)
        self.connect.commit()

    def update(self, SQL, *args):
        pass

    def close(self):
        self.cursor.close()
        self.connect.close()

def get_count_pswd(db):
    """return count and password from database(db)."""
    SQL = "select * from CUMTB order by random() limit 1;"
    database = DB(db)
    select_res = database.select(SQL)[0]
    database.close()

    return select_res


def write_conf(count, password):
    if 'linux' in sys_version():
        os.system("./encrypt {0} {1}".format(count, password))
    elif 'win' in sys.platform:
        os.system(".\encrypt.exe {0} {1}".format(count, password))

def abu_login(db):
    """
    isinstance a Drcom class, and login Drcom,
    return login status and Drcom isinstance.
    (status, isinstance)
    """
    main = Drcom()
    main.login()
    database = DB(db)
    if main.IS_LOGIN and main.balance > 4000:
        main.LOG.warning("Loged in as count: {0}, password: {1}".format(
            main.count, main.password))
        main.LOG.warning('Used {0} MBytes, {1} MBytes balanced'.format(
            main.used, main.balance))
    else:
        main.IS_LOGIN = False
        main.LOG.warn('Login failed...')
        database.delete("delete from CUMTB where Sno=?", main.count)
        main.LOG.warning("delete {} from database.".format(main.count))

    database.close()
    return main.IS_LOGIN, main, main.balance

def start():
    LOGED_IN = False
    while not LOGED_IN:
        count, password = get_count_pswd("CUMTB.db")
        write_conf(count, password)
        return abu_login("CUMTB.db")


if __name__ == "__main__":
    CONTINUE = True
    while CONTINUE:
        status, sess, balance = start()
        start_time = time.time()
        while ((time.time() - start_time) < 2700) and CONTINUE:
            time.sleep(0.5)
            try:
                sess.get_user_message()
            except IndexError:
                break
            except KeyboardInterrupt:
                CONTINUE = False
                start()[1].LOG.warn("Bye.")
