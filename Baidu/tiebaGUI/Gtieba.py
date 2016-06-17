#!/usr/bin/env python
#  coding=utf-8
import Tkinter as tk
import TiebaGUI

root = tk.Tk()
root.title(u"Tieba")
root.geometry('400x400')
tk.Label(root, text="Tieba by x1ah", pady=20).pack()


User = tk.Label(root, text="手机号/邮箱/用户名：")
User.pack()
usr = tk.StringVar()

usr_input = tk.Entry(root, textvariable=usr, width=36, bd=5)
usr_input.pack()

Pswd = tk.Label(root, text="密码：")
Pswd.pack()
pswd = tk.StringVar()

pswd_input = tk.Entry(root, textvariable=pswd, width=36, bd=5)
pswd_input['show'] = '*'
pswd_input.pack()

def get_text():
    return TiebaGUI.start(usr.get(), pswd.get())

def print_content():
    text_output.delete(0.0, 'end')
    text_output.insert(0.0, 'succeed!')
    text_output.insert(0.0, get_text())
    usr.set('')
    pswd.set('')

tk.Button(root,text=u"开始签到", command=print_content).pack()
print u'正在签到...'
root.bind('<Return>', lambda event:print_content())

text_output = tk.Text(root, width=500)
text_output.pack(side='left', fill='y')

s = tk.Scrollbar(root)
s.pack(side='right', fill='y')

s.config(command=text_output.yview)
text_output.config(yscrollcommand=s.set)

root.mainloop()
