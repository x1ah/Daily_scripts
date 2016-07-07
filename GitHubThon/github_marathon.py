#!/usr/bin/env python
# coding:utf-8
import time
import os
from os import system
from os import popen
from time import ctime
from json import loads
from json import dumps


class CreatCommit(object):

    def __init__(self):
        pass

    def work_space(self):
        os.chdir('/root/Daily_scripts/GitHubThon/')

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
        with open('marathon.json', 'w') as new:
            new_json = dumps(pre_json, indent=4)
            new.write(new_json)
        return new_json

    def git_push(self):
        system("git add .")
        system("git commit -m'commit by robot'")
        time.sleep(2)
        system("git push")

    def run(self):
        try:
            pre_json = self.read_json()
            self.write_json(pre_json)
            self.git_push()
        except:
            pass

if __name__ == '__main__':
    new_commit = CreatCommit()
    new_commit.work_space()
    new_commit.run()
