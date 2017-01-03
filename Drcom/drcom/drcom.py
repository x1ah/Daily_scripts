#!/usr/bin/env python
# coding:utf-8

import re
import json
import random
import contextlib

from .utils import Base

@contextlib.contextmanager
def ignored(*exceptions):
    try:
        yield
    except:
        pass

class Drcom(Base):

    def __init__(self):
        super(Drcom, self).__init__()
        self.url_base = "http://202.112.208.3/"
        self.IS_LOGIN = False

    @staticmethod
    def get_count_pswd():
        with open("there_is_nothing.json", 'r') as f:
            infos = json.load(f)
        return infos[random.randint(0, len(infos))], infos

    @staticmethod
    def update_conf(data, path="there_is_nothing.json"):
        with open(path, 'w') as f:
            json.dump(data, f)

    @staticmethod
    def delete_count(data, path="there_is_nothing.json"):
        _, infos = Drcom.get_count_pswd()
        infos.remove(data)
        Drcom.update_conf(infos)

    def login(self):
        user_info, _ = self.get_count_pswd()
        self.user_info = user_info
        self.count = user_info.get("count")
        self.pswd = user_info.get("password")
        form_data = {
            "DDDDD": user_info.get("count"),
            "upass": user_info.get("enpassword"),
            "R1": "0",
            "R2": "1",
            "para": "00",
            "0MKKey": "123456"
        }
        response = self.http_request.post(self.url_base,data=form_data)
        self.IS_LOGIN = "You have successfully logged into our system"\
            in response.text
        return self.IS_LOGIN

    def logout(self):
        response = self.http_request.get(self.url_base+"F.htm")
        self.IS_LOGIN = "can not modify" in response.content

    def get_user_info(self):
        html = self.http_request.get(self.url_base).text
        flow = int(re.findall("flow=\'(\d+)", html)[0])
        used = self.calc_flow(flow)
        self.used , self.balance = used, 25600 - used

    @staticmethod
    def calc_flow(flow):
        flow0 = flow % 1024
        flow1 = flow - flow0
        flow0 = flow0 * 1000
        flow0 = flow0 - flow0 % 1024
        return float('{0}.{1}'.format(flow1 // 1024, flow0 // 1024))
