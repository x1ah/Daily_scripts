#!/usr/bin/env python
# coding:utf-8
from bs4 import BeautifulSoup
import requests
import re
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')

def Soup(session, url):
    html = session.get(url)
    soup = BeautifulSoup(html.text, 'lxml')
    return soup

def login(username, pswd='0'):
    '''
    模拟登录教务系统
    :param username:
    :param pswd:
    :return: 登录状态
    '''
    login_url = 'http://219.242.68.33/Login.aspx'
    from_data = {
        "ToolkitScriptManager1_HiddenField": "",
        "__EVENTTARGET": "",
        "__EVENTARGUMENT": "",
        "__VIEWSTATE": "/wEPDwUKMTY0Njg4MjEwM2Rkj+Af8kaVOxsefGZECk5PM6rOOYgs0taVhQxQSxoC298=",
        "__VIEWSTATEGENERATOR": "C2EE9ABB",
        "__EVENTVALIDATION": "/wEWCQKK9JioBQLB2tiHDgK1qbSRCwLB9fLCCQKVwf3jAwL7jJeqDQK2yLNyAoyp3LQNAoLch4YM4/7Gzd6qXWcFlpTQVOKRLsJcEeZ1kj5lh7u9AQrHyms=",
        "txtUser": username,
        "txtPassword": pswd,
        "rbLx": "学生",
        "btnLogin": " 登 录 "
    }
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.86 Safari/537.36"
    }

    s = requests.session()
    response = s.post(url=login_url, data=from_data, headers=header)
    response_text = response.text
    if response_text.find('个人资料') > 0:
        print '登录成功！'
        return s
    elif response_text.find('密码不正确') > 0:
        print '密码错误...请重试...'
        return False
    else:
        print '登录失败...请重试...'
        return False

def get_ifo(sess):
    '''
    通过登录会话session获取学生信息
    :param sess:
    :return: 学生信息
    '''
    ifo_url = 'http://219.242.68.33/xuesheng/xsxx.aspx'
    soup = Soup(sess, ifo_url)
    data = {}
    data['a.姓名'] = soup.find(id="ctl00_ContentPlaceHolder1_lblXm").text
    data['b.身份证号'] = soup.find(id="ctl00_ContentPlaceHolder1_lblSfz").text
    data['c.学号'] = soup.find(id="ctl00_ContentPlaceHolder1_lblXh").text
    data['d.班级'] = soup.find(id="ctl00_ContentPlaceHolder1_className").text
    data['e.院系'] = soup.find(id="ctl00_ContentPlaceHolder1_collegeName").text
    for item in sorted(data):
        print '{0}:{1}{2}'.format(item, '-'*5, data[item])

def get_score(sess):
    score_url = 'http://219.242.68.33/xuesheng/cjcx.aspx'
    soup = Soup(sess, score_url)
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
    print '平均成绩:{0}\n课程门数:{1}\n已获得学分:{2}\n'.format(average, total, credit)
    for index, year, term, unit, nature, course, score in \
            zip(indexs, years, terms, units, natures, courses, scores):
        # 打印对齐，使整体美观
        if len(course) < 7:
            s = '序号:{0}\t||课程: {1}||\t\t成绩:{2}\t 学分:{3}\t || {4} {5} {6}\n' \
            .format(index, course, score.replace('\n', ' '), unit, year, term, nature)
        elif len(course) <= 10:
            s = '序号:{0}\t||课程: {1}||\t成绩:{2}\t 学分:{3}\t || {4} {5} {6}\n' \
            .format(index, course, score.replace('\n', ' '), unit, year, term, nature)
        else:
            s = '序号:{0}\t||课程: {1}||成绩:{2}\t 学分:{3}\t || {4} {5} {6}\n' \
            .format(index, course, score.replace('\n', ' '), unit, year, term, nature)
        print s
    print '平均成绩:{0}\n课程门数:{1}\n已获得学分:{2}\n'.format(average, total, credit)

def elective(sess):
    eleurl = 'http://219.242.68.33/xuesheng/xsxk.aspx'
    from_data= {
        "__EVENTTARGET": "",
        "__EVENTARGUMENT": "",
        "__VIEWSTATE": "/wEPDwULLTE1NDU0NjAxMDUPZBYCZg9kFgICAw9kFgICAQ9kFgICAw8QDxYGHg1EYXRhVGV4dEZpZWxkBQRrenNtHg5EYXRhVmFsdWVGaWVsZAUDa3poHgtfIURhdGFCb3VuZGdkEBUdFzE1LTE256ys5LqM5a2m5pyf5YWs6YCJFzE1LTE256ys5LiA5a2m5pyf5YWs6YCJFzE0LTE156ys5LqM5a2m5pyf5YWs6YCJFzE0LTE156ys5LiA5a2m5pyf5YWs6YCJFzEzLTE056ys5LqM5a2m5pyf5YWs6YCJFzEzLTE056ys5LiA5a2m5pyf5YWs6YCJGeiLseivree7vOWQiOaKgOiDveWfueWFuzEXMTItMTPnrKzkuozlrabmnJ/lhazpgIkZ6Iux6K+t57u85ZCI5oqA6IO95Z+55YW7MRcxMi0xM+esrOS4gOWtpuacn+WFrOmAiRcxMS0xMuesrOS6jOWtpuacn+WFrOmAiRcxMS0xMuesrOS4gOWtpuacn+WFrOmAiRcxMC0xMeesrOS6jOWtpuacn+WFrOmAiRcxMC0xMeesrOS4gOWtpuacn+WFrOmAiRcwOS0xMOesrOS6jOWtpuacn+WFrOmAiRcwOS0xMOesrOS4gOWtpuacn+WFrOmAiRcwOC0wOeesrOS6jOWtpuacn+WFrOmAiRcwOC0wOeesrOS4gOWtpuacn+WFrOmAiRcwNy0wOOesrOS6jOWtpuacn+WFrOmAiRcwNy0wOOesrOS4gOWtpuacn+WFrOmAiRcwNi0wN+esrOS6jOWtpuacn+WFrOmAiRcwNi0wN+esrOS4gOWtpuacn+WFrOmAiRcwNS0wNuesrOS6jOWtpuacn+WFrOmAiRcwNS0wNuesrOS4gOWtpuacn+WFrOmAiRcwNC0wNeesrOS6jOWtpuacn+WFrOmAiRcwNC0wNeesrOS4gOWtpuacn+WFrOmAiRcwMy0wNOesrOS6jOWtpuacn+WFrOmAiRcwMy0wNOesrOS4gOWtpuacn+WFrOmAiRcwMi0wM+esrOS6jOWtpuacn+WFrOmAiRUdAzMyMQMzMTgDMzE0AzMxMwMzMDIDMjQzAzI0MgMyNDEDMjQwAzIzOQMyMzgDMjM3AzIzNgMyMzUDMjM0AzIzMwMyMzIDMjMxAzIzMAMyMjkDMjI4AzIyNwMyMjYDMjE2AzIxNQMyMTQDMjEzAzIxMgMyMTAUKwMdZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2cWAWZkZBgWDkNmM5ksFZPYJS+CXe3IihlDoFim1X/o3cfNS5fN",
        "__VIEWSTATEGENERATOR": "E7E695A4",
        "ctl00$ContentPlaceHolder1$drplKcz": '321',
        "ctl00$ContentPlaceHolder1$btnYxkc": "查 看"
    }
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.86 Safari/537.36"
    }
    ss = sess.post(eleurl, data=from_data, headers=header)
    soup = BeautifulSoup(ss.text, 'lxml')
    all_num = soup.find_all('td')
    all_item = [item.text for item in all_num]
    indexs = all_item[1::5]
    times = [item[4:].strip() for item in all_item[2::5]]
    courses = [item.split()[0] for item in all_item[4::5]]
    teachers = [item.split()[1] for item in all_item[4::5]]
    for index, time, course, teacher in zip(indexs, times, courses, teachers):
        s = '序号: {0}{1} | 课程组: {2}{3} | 课程名称: {4}(任课教师: {5})'.format(index, '\t', time, '\t', course, teacher)
        print s

def Quit():
    '''
    退出
    :return: None
    '''
    print 'Quited...'
    os.system('clear')

def main():
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
    username = raw_input('学号: ')
    pswd = raw_input('密码: 00000000\b\b\b\b\b\b\b\b')
    sess = login(username, pswd)
    if sess:
        choice = True
        choice_dict = {
            '1': get_score,
            '2': get_ifo,
            '3': elective,
        }
        while choice:
            try:
                usr_choice = raw_input('\r'+prompt).strip()[0]
                os.system('clear')
                print '*' * 80
                if usr_choice in choice_dict:
                    choice_dict[usr_choice](sess)
                elif usr_choice == '4':
                    main()
                    choice = False
                elif usr_choice == '5':
                    os.system('clear')
                elif usr_choice == '6':
                    Quit()
                    choice = False
                else:
                    print 'Input incorrect..again!'
            except:
                print 'Input Error..'
    else:
        cho = raw_input('Cotinue or not [n/y]: ').strip()[0]
        if cho == 'y':
            main()
        else:
            Quit()

if __name__ == '__main__':
    os.system('clear')
    main()
