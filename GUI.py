import os
import sys
from tkinter import *
from tkinter.messagebox import showinfo


def reply(name):
    showinfo(title='GUI测试', message='你好！ %s' % name)


# 应用窗口
window = Tk()

window.title('获取用户输入：郑雄')  # 窗口标题

# window.iconbitmap('py-blue-trans-out.ico') #自定义窗体的图标

Label(window, text='输入你的名字：').pack(side=TOP)

ent = Entry(window)

ent.pack(side=TOP)

button = Button(window, text='确定', command=(lambda: reply(ent.get())))

button.pack(side=LEFT)

window.mainloop()
