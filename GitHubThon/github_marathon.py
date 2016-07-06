#!/usr/bin/env python
# coding:utf-8
from os import system
from time import ctime
from time import sleep
from json import loads


class CreatCommit(object):

    def __init__(self):
        pass

    def read_json(self):
        with open('marathon.json', 'r') as file_data:
            pre_data = file_data.read()
            pre_json = loads(pre_data)
        return pre_json

    def write_json(self, pre_json):
        times = int(pre_json['commit_times']) + 1
        start_from = pre_json['first_robot_commit']
        start_from = ctime() if not start_from else start_from
        pre_json['current_time'] = ctime()
        pre_json['commit_times'] = times
        pre_json['first_robot_commit'] = start_from
        print pre_json
        with open('marathon.json', 'w') as new:
            new.write(str(pre_json))
        return pre_json

    def git_push(self):
        system("git add .")
        sleep(1)
        system("git commit -m'commit from robot'")
        sleep(1)
        system("git push")

    def run(self):
        #try:
        pre_json = self.read_json()
        self.write_json(pre_json)
        self.git_push()
        #except:

if __name__ == '__main__':
    new_commit = CreatCommit()
    new_commit.run()
