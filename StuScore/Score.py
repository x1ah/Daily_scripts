#!/usr/bin/env python
# coding:utf-8

import os

from bs4 import BeautifulSoup

from utils import (Soup, HTTPRequest, table_print, validate_login,
                   quit, clear, rinput)


class Score:
    def __init__(self, usrname='0', usrpswd='0', user_type=u"学生",
                 display=True):
        self.usrname = usrname
        self.usrpswd = usrpswd
        self.user_type = user_type
        self.display = display
        self.http_request = HTTPRequest()


    def login(self):
        '''
        模拟登录教务系统
        :param username:
        :param pswd:
        :return: 登录状态
        '''
        login_url = 'http://219.242.68.33/Login.aspx'

        form_data = {
            "ToolkitScriptManager1": "ToolkitScriptManager1|btnLogin",
            "ToolkitScriptManager1_HiddenField": "",
            "__EVENTTARGET": "",
            "__EVENTARGUMENT": "",
            "__VIEWSTATE": (
                "/wEPDwULLTEzMzI5MDg5NTdkZA+q8vsWfSKH/YDs"
                "W+RwQFVd+XJey2nS+KBASrL5sVcV"
            ),
            "__VIEWSTATEGENERATOR": "C2EE9ABB",
            "__EVENTVALIDATION": (
                "/wEWCQKBn//oBgLB2tiHDgK1qbSRCwLB9f"
                "LCCQKVwf3jAwL7jJeqDQK2yLNyAoyp3LQN"
                "AoLch4YMPGB+WTKjbk2vdv7fTF2wbC+5yb"
                "bEOCiOGr7YY8J7e8o="
            ),
            "txtUser": self.usrname,
            "txtPassword": self.usrpswd,
            "rbLx": self.user_type,
            "__ASYNCPOST": "true",
            "btnLogin": " 登 录 "
        }


        response = self.http_request.post(login_url, data=form_data).text
        return validate_login(
            response,
            validator={
                "pageRedirect": [True, "登录成功"],
                u"密码不正确": [False, "密码错误"],
            },
            default=[False, "登录失败"]
        )

    def get_info(self):
        '''
        通过登录会话session获取学生信息
        :param sess:
        :return: 学生信息
        '''
        ifo_url = 'http://219.242.68.33/xuesheng/xsxx.aspx'
        soup = Soup(self.http_request.session, ifo_url)
        data = {}
        data['a.姓名'] = soup.find(id="ctl00_ContentPlaceHolder1_lblXm").text
        data['b.身份证号'] = soup.find(id="ctl00_ContentPlaceHolder1_lblSfz").text
        data['c.学号'] = soup.find(id="ctl00_ContentPlaceHolder1_lblXh").text
        data['d.班级'] = soup.find(id="ctl00_ContentPlaceHolder1_className").text
        data['e.院系'] = soup.find(id="ctl00_ContentPlaceHolder1_collegeName").text
        if self.display is True:
            tabletitle = [item[2:] for item in sorted(data.keys())]
            cont = [data[item] for item in sorted(data.keys())]
            table_print(tabletitle, cont)

        return data

    def get_score(self):
        score_url = 'http://219.242.68.33/xuesheng/cjcx.aspx'
        soup = Soup(self.http_request.session, score_url)
        all_scoreifo = [item.text.strip() for item in soup.find_all('td')]
        indexs = all_scoreifo[0::10]
        years = all_scoreifo[2::10]
        terms = all_scoreifo[3::10]
        units = all_scoreifo[5::10]
        natures = all_scoreifo[7::10]
        courses = all_scoreifo[8::10]
        scores = map(lambda x: ' / '.join(x),
                     [item.split('\n') for item in all_scoreifo[9::10]])
        average = soup.find(id="ctl00_ContentPlaceHolder1_lblpjcj").text
        total = soup.find(id="ctl00_ContentPlaceHolder1_lblKcms").text
        credit = soup.find( id="ctl00_ContentPlaceHolder1_lblXfs").text

        tabletitle = ['序号', '课程', '成绩', '学分', '学年', '学期', '性质']
        conts = []

        for index, year, term, unit, nature, course, score in \
                zip(indexs, years, terms, units, natures, courses, scores):
            temp = [index, course.strip(), score.replace('\n', ''), unit, year, term, nature]
            conts.append(temp)
        if self.display:
            table_print(tabletitle, conts)
            table_print(['平均成绩','课程门数', '已获得学分'], [[average, total, credit]])
        return conts

    def elective(self):
        """
        获取选修课信息
        """
        eleurl = 'http://219.242.68.33/xuesheng/xsxk.aspx'
        form_data= {
            "__EVENTTARGET": "",
            "__EVENTARGUMENT": "",
            "__VIEWSTATE": (
                "/wEPDwULLTE1NDU0NjAxMDUPZBYCZg9kFgICAw9kFgICAQ9kFgIC"
                "Aw8QDxYGHg1EYXRhVGV4dEZpZWxkBQRrenNtHg5EYXRhVmFsdWVG"
                "aWVsZAUDa3poHgtfIURhdGFCb3VuZGdkEBUdFzE1LTE256ys5LqM"
                "5a2m5pyf5YWs6YCJFzE1LTE256ys5LiA5a2m5pyf5YWs6YCJFzE0"
                "LTE156ys5LqM5a2m5pyf5YWs6YCJFzE0LTE156ys5LiA5a2m5pyf"
                "5YWs6YCJFzEzLTE056ys5LqM5a2m5pyf5YWs6YCJFzEzLTE056ys"
                "5LiA5a2m5pyf5YWs6YCJGeiLseivree7vOWQiOaKgOiDveWfueWF"
                "uzEXMTItMTPnrKzkuozlrabmnJ/lhazpgIkZ6Iux6K+t57u85ZCI"
                "5oqA6IO95Z+55YW7MRcxMi0xM+esrOS4gOWtpuacn+WFrOmAiRcx"
                "MS0xMuesrOS6jOWtpuacn+WFrOmAiRcxMS0xMuesrOS4gOWtpuac"
                "n+WFrOmAiRcxMC0xMeesrOS6jOWtpuacn+WFrOmAiRcxMC0xMees"
                "rOS4gOWtpuacn+WFrOmAiRcwOS0xMOesrOS6jOWtpuacn+WFrOmA"
                "iRcwOS0xMOesrOS4gOWtpuacn+WFrOmAiRcwOC0wOeesrOS6jOWt"
                "puacn+WFrOmAiRcwOC0wOeesrOS4gOWtpuacn+WFrOmAiRcwNy0w"
                "OOesrOS6jOWtpuacn+WFrOmAiRcwNy0wOOesrOS4gOWtpuacn+WF"
                "rOmAiRcwNi0wN+esrOS6jOWtpuacn+WFrOmAiRcwNi0wN+esrOS4"
                "gOWtpuacn+WFrOmAiRcwNS0wNuesrOS6jOWtpuacn+WFrOmAiRcw"
                "NS0wNuesrOS4gOWtpuacn+WFrOmAiRcwNC0wNeesrOS6jOWtpuac"
                "n+WFrOmAiRcwNC0wNeesrOS4gOWtpuacn+WFrOmAiRcwMy0wNOes"
                "rOS6jOWtpuacn+WFrOmAiRcwMy0wNOesrOS4gOWtpuacn+WFrOmA"
                "iRcwMi0wM+esrOS6jOWtpuacn+WFrOmAiRUdAzMyMQMzMTgDMzE0"
                "AzMxMwMzMDIDMjQzAzI0MgMyNDEDMjQwAzIzOQMyMzgDMjM3AzIz"
                "NgMyMzUDMjM0AzIzMwMyMzIDMjMxAzIzMAMyMjkDMjI4AzIyNwMy"
                "MjYDMjE2AzIxNQMyMTQDMjEzAzIxMgMyMTAUKwMdZ2dnZ2dnZ2dn"
                "Z2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2cWAWZkZBgWDkNmM5ksFZPYJS+C"
                "Xe3IihlDoFim1X/o3cfNS5fN"
            ),
            "__VIEWSTATEGENERATOR": "E7E695A4",
            "ctl00$ContentPlaceHolder1$drplKcz": '321',
            "ctl00$ContentPlaceHolder1$btnYxkc": "查 看"
        }
        ss = self.http_request.post(eleurl, data=form_data)
        soup = BeautifulSoup(ss.text, 'lxml')
        all_num = soup.find_all('td')
        all_item = [item.text for item in all_num]
        indexs = all_item[1::5]
        times = [item[4:].strip() for item in all_item[2::5]]
        courses = [item.split()[0] for item in all_item[4::5]]
        teachers = [item.split()[1] for item in all_item[4::5]]
        tabletitle = ['序号', '课程组', '课程名称', '任课教师']
        conts = []
        for index, time, course, teacher in zip(indexs, times, courses, teachers):
            temp = [index, time, course, teacher]
            conts.append(temp)
        if self.display:
            table_print(tabletitle, conts)

    def cli(self):
        prompt = '''
        +===========================+
        |   [0]查成绩               |
        |   [1]个人信息             |
        |   [2]选修课               |
        |   [3]登录其他账号         |
        |   [4]清除历史记录         |
        |   [5]安全退出             |
        +===========================+
        >>> '''
        self.usrname = rinput('学号: ')
        self.usrpswd = rinput('密码: 00000000\b\b\b\b\b\b\b\b')

        status = self.login()
        if status[0]:
            choice = True
            choice_dict = {
                '0': self.get_score,
                '1': self.get_info,
                '2': self.elective,
                '3': self.cli,
                '4': clear,
                '5': quit
            }
            while choice is True:
                usr_choice = rinput('\r'+prompt).strip()[0]
                os.system('clear')
                if usr_choice in choice_dict:
                    choice_dict.get(usr_choice)()
                    choice = usr_choice not in "35"
                else:
                    print('Input incorrect..again!')
        else:
            print(status[1])

            cho = rinput('Any key to continue, [q] to quit.')

            if cho == 'q':
                quit()
            else:
                self.cli()

if __name__ == '__main__':
    os.system('clear')
    start = Score()
    start.cli()
