#!/usr/bin/env python
# coding:utf-8
from bs4 import BeautifulSoup
from prettytable import PrettyTable
import requests, os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class score(object):
    def __init__(self, usrname='0', usrpswd='0', display=True):
        self.usrname = usrname
        self.usrpswd = usrpswd
        self.display = display

    def Soup(self, session, url):
        html = session.get(url)
        soup = BeautifulSoup(html.text, 'lxml')
        return soup

    def login(self):
        '''
        模拟登录教务系统
        :param username:
        :param pswd:
        :return: 登录状态
        '''
        login_url = 'http://219.242.68.33/Login.aspx'
        form_data = {
            "ToolkitScriptManager1_HiddenField": "",
            "__EVENTTARGET": "",
            "__EVENTARGUMENT": "",
            "__VIEWSTATE": "/wEPDwUKMTY0Njg4MjEwM2Rkj+Af8kaVOxsefGZECk5PM6rOOYgs0taVhQxQSxoC298=",
            "__VIEWSTATEGENERATOR": "C2EE9ABB",
            "__EVENTVALIDATION": "/wEWCQKK9JioBQLB2tiHDgK1qbSRCwLB9fLCCQKVwf3jAwL7jJeqDQK2yLNyAoyp3LQNAoLch4YM4/7Gzd6qXWcFlpTQVOKRLsJcEeZ1kj5lh7u9AQrHyms=",
            "txtUser": self.usrname,
            "txtPassword": self.usrpswd,
            "rbLx": "学生",
            "btnLogin": " 登 录 "
        }
        header = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.86 Safari/537.36"
        }
        self.headers = header
        s = requests.session()
        response = s.post(url=login_url, data=form_data, headers=header)
        response_text = response.text
        if response_text.find(u'个人资料') > 0:
            ifo = '登录成功！'
            status = s
        elif response_text.find('密码不正确') > 0:
            ifo = '密码错误...请重试...'
            status = False
        else:
            ifo = '登录失败...请重试...'
            status = False
        if self.display is True:
            print ifo
        return status

    def tableprint(self, title, conts):
        table = PrettyTable(title)
        table.padding_width = 2
        if type(conts[0]) is list:
            [table.add_row(cont) for cont in conts]
        else:
            table.add_row(conts)
        print(table)

    def get_ifo(self, sess):
        '''
        通过登录会话session获取学生信息
        :param sess:
        :return: 学生信息
        '''
        ifo_url = 'http://219.242.68.33/xuesheng/xsxx.aspx'
        soup = self.Soup(sess, ifo_url)
        data = {}
        data['a.姓名'] = soup.find(id="ctl00_ContentPlaceHolder1_lblXm").text
        data['b.身份证号'] = soup.find(id="ctl00_ContentPlaceHolder1_lblSfz").text
        data['c.学号'] = soup.find(id="ctl00_ContentPlaceHolder1_lblXh").text
        data['d.班级'] = soup.find(id="ctl00_ContentPlaceHolder1_className").text
        data['e.院系'] = soup.find(id="ctl00_ContentPlaceHolder1_collegeName").text
        if self.display is True:
            tabletitle = [item[2:] for item in sorted(data.keys())]
            cont = [data[item] for item in sorted(data.keys())]
            self.tableprint(tabletitle, cont)

        return data

    def get_score(self, sess):
        score_url = 'http://219.242.68.33/xuesheng/cjcx.aspx'
        soup = self.Soup(sess, score_url)
        all_scoreifo = [item.text.strip() for item in soup.find_all('td')]
        indexs = all_scoreifo[0::10]
        years = all_scoreifo[2::10]
        terms = all_scoreifo[3::10]
        units = all_scoreifo[5::10]
        natures = all_scoreifo[7::10]
        courses = all_scoreifo[8::10]
        scores = all_scoreifo[9::10]
        average = soup.find(id="ctl00_ContentPlaceHolder1_lblpjcj").text
        total = soup.find(id="ctl00_ContentPlaceHolder1_lblKcms").text
        credit = soup.find( id="ctl00_ContentPlaceHolder1_lblXfs").text

        tabletitle = ['序号', '课程', '成绩', '学分', '学年', '学期', '性质']
        conts = []

        for index, year, term, unit, nature, course, score in \
                zip(indexs, years, terms, units, natures, courses, scores):
            temp = [index, course.strip(), score.replace('\n', ''), unit, year, term, nature]
            conts.append(temp)
        self.tableprint(tabletitle, conts)
        self.tableprint(['平均成绩','课程门数', '已获得学分'], [[average, total, credit]])

    def elective(self, sess):
        eleurl = 'http://219.242.68.33/xuesheng/xsxk.aspx'
        form_data= {
            "__EVENTTARGET": "",
            "__EVENTARGUMENT": "",
            "__VIEWSTATE": "/wEPDwULLTE1NDU0NjAxMDUPZBYCZg9kFgICAw9kFgICAQ9kFgICAw8QDxYGHg1EYXRhVGV4dEZpZWxkBQRrenNtHg5EYXRhVmFsdWVGaWVsZAUDa3poHgtfIURhdGFCb3VuZGdkEBUdFzE1LTE256ys5LqM5a2m5pyf5YWs6YCJFzE1LTE256ys5LiA5a2m5pyf5YWs6YCJFzE0LTE156ys5LqM5a2m5pyf5YWs6YCJFzE0LTE156ys5LiA5a2m5pyf5YWs6YCJFzEzLTE056ys5LqM5a2m5pyf5YWs6YCJFzEzLTE056ys5LiA5a2m5pyf5YWs6YCJGeiLseivree7vOWQiOaKgOiDveWfueWFuzEXMTItMTPnrKzkuozlrabmnJ/lhazpgIkZ6Iux6K+t57u85ZCI5oqA6IO95Z+55YW7MRcxMi0xM+esrOS4gOWtpuacn+WFrOmAiRcxMS0xMuesrOS6jOWtpuacn+WFrOmAiRcxMS0xMuesrOS4gOWtpuacn+WFrOmAiRcxMC0xMeesrOS6jOWtpuacn+WFrOmAiRcxMC0xMeesrOS4gOWtpuacn+WFrOmAiRcwOS0xMOesrOS6jOWtpuacn+WFrOmAiRcwOS0xMOesrOS4gOWtpuacn+WFrOmAiRcwOC0wOeesrOS6jOWtpuacn+WFrOmAiRcwOC0wOeesrOS4gOWtpuacn+WFrOmAiRcwNy0wOOesrOS6jOWtpuacn+WFrOmAiRcwNy0wOOesrOS4gOWtpuacn+WFrOmAiRcwNi0wN+esrOS6jOWtpuacn+WFrOmAiRcwNi0wN+esrOS4gOWtpuacn+WFrOmAiRcwNS0wNuesrOS6jOWtpuacn+WFrOmAiRcwNS0wNuesrOS4gOWtpuacn+WFrOmAiRcwNC0wNeesrOS6jOWtpuacn+WFrOmAiRcwNC0wNeesrOS4gOWtpuacn+WFrOmAiRcwMy0wNOesrOS6jOWtpuacn+WFrOmAiRcwMy0wNOesrOS4gOWtpuacn+WFrOmAiRcwMi0wM+esrOS6jOWtpuacn+WFrOmAiRUdAzMyMQMzMTgDMzE0AzMxMwMzMDIDMjQzAzI0MgMyNDEDMjQwAzIzOQMyMzgDMjM3AzIzNgMyMzUDMjM0AzIzMwMyMzIDMjMxAzIzMAMyMjkDMjI4AzIyNwMyMjYDMjE2AzIxNQMyMTQDMjEzAzIxMgMyMTAUKwMdZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2cWAWZkZBgWDkNmM5ksFZPYJS+CXe3IihlDoFim1X/o3cfNS5fN",
            "__VIEWSTATEGENERATOR": "E7E695A4",
            "ctl00$ContentPlaceHolder1$drplKcz": '321',
            "ctl00$ContentPlaceHolder1$btnYxkc": "查 看"
        }
        ss = sess.post(eleurl, data=form_data, headers=self.headers)
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
        self.tableprint(tabletitle, conts)

    def Quit(self):
        '''
        退出
        :return: None
        '''
        print 'Quited...'
        os.system('clear')

    def main(self):
        prompt = '''
        +===========================+
        |   [1]查成绩               |
        |   [2]个人信息             |
        |   [3]选修课               |
        |   [4]登录其他账号         |
        |   [5]清除历史记录         |
        |   [6]安全退出             |
        +===========================+
        >>> '''
        self.usrname = raw_input('学号: ')
        self.usrpswd = raw_input('密码: 00000000\b\b\b\b\b\b\b\b')
        sess = self.login()
        if sess:
            choice = True
            choice_dict = {
                '1': self.get_score,
                '2': self.get_ifo,
                '3': self.elective,
            }
            while choice is True:
#                try:
                usr_choice = raw_input('\r'+prompt).strip()[0]
                os.system('clear')
                print '*' * 80
                if usr_choice in choice_dict:
                    choice_dict[usr_choice](sess)
                elif usr_choice == '4':
                    self.main()
                    choice = False
                elif usr_choice == '5':
                    os.system('clear')
                elif usr_choice == '6':
                    self.Quit()
                    choice = False
                else:
                    print 'Input incorrect..again!'
        else:
            cho = raw_input('[q] to Quit.')
            if cho != 'q':
                self.main()
            else:
                self.Quit()

if __name__ == '__main__':
    os.system('clear')
    start = score()
    start.main()
