#!/usr/bin/env python
# coding:utf-8
from bs4 import BeautifulSoup
import requests
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

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
    html = sess.get(ifo_url)
    soup = BeautifulSoup(html.text, 'lxml')
    data = {}
    data['a.姓名'] = soup.find(id="ctl00_ContentPlaceHolder1_lblXm").text
    data['b.身份证号'] = soup.find(id="ctl00_ContentPlaceHolder1_lblSfz").text
    data['c.学号'] = soup.find(id="ctl00_ContentPlaceHolder1_lblXh").text
    data['d.班级'] = soup.find(id="ctl00_ContentPlaceHolder1_className").text
    data['e.院系'] = soup.find(id="ctl00_ContentPlaceHolder1_collegeName").text
    for item in sorted(data):
        print '{0}:{1}{2}'.format(item, '-'*5, data[item])


def get_score(username, pswd='0'):
    pass

def elective(username, pswd):
    pass

def Quit():
    '''
    退出
    :return: None
    '''
    print 'Quited...'

def main():
    prompt = '''
    +===========================+
    |   [1]查成绩               |
    |   [2]个人信息             |
    |   [3]选修课               |
    |   [4]登录其他账号         |
    |   [5]安全退出             |
    +===========================+
    >>> '''
    username = raw_input('学号: ')
    pswd = raw_input('密码: ')
    sess = login(username, pswd)
    if sess:
        choice = True
        while choice:
            usr_choice = raw_input('\r'+prompt).strip()[0]
            if usr_choice == '1':
                get_score(sess, username, pswd)
            elif usr_choice == '2':
                get_ifo(sess)
            elif usr_choice == '3':
                elective(sess, username, pswd)
            elif usr_choice == '4':
                main()
                break
            elif usr_choice == '5':
                Quit()
                break
            else:
                print 'Input incorrect..again!'
    else:
        cho = raw_input('Cotinue or not [n/y]: ').strip()[0]
        if cho == 'y':
            main()
        else:
            Quit()

if __name__ == '__main__':
    main()
