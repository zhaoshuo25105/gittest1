#coding:utf-8
import pickle  # 存放数据的模块
import tkinter as tk
import tkinter.messagebox
from user import *
from leader import *
from super_user import *
from super_user_1 import *
from user_attclient import *
import time,datetime
from PIL import ImageTk, Image


root = tk.Tk()
root.title("员工自助管理系统")
root.geometry("450x300+300+200")
root.resizable(False, False) 

canvas = tk.Canvas(root, width=450,height=300,bd=0, highlightthickness=0)
imgpath = '1.gif'
img = Image.open(imgpath)
photo = ImageTk.PhotoImage(img)
 
canvas.create_image(0, 0, anchor='nw',image=photo)
canvas.pack()

tk.Label(root, text='账号:').place(x=110, y=125)
tk.Label(root, text='密码:').place(x=110, y=165)
 
var_usr_name = tk.StringVar()
var_usr_name.set('l1001')
var_usr_pwd = tk.StringVar()
var_usr_pwd.set('lixinkui')
 
entry_usr_name = tk.Entry(root, textvariable=var_usr_name)
entry_usr_name.place(x=190, y=125)
entry_usr_pwd = tk.Entry(root, textvariable=var_usr_pwd, show='*')
entry_usr_pwd.place(x=190, y=165)

s.connect(address_user)
def usr_login():
    user = var_usr_name.get()
    passwd = var_usr_pwd.get()
    if user == '1q2w3e':
        res = main(s,user,passwd)
        if res == 'OK':
            tk.messagebox.showinfo(title='欢迎!!',message=user+'您好!')
            root.destroy()
            show_superuser_menu(user)
        else: 
            tk.messagebox.showinfo(message='您输入有误,请重新输入!')
    elif user[0:1] == 'n':
        res = main1(s,user,passwd)
        if res == 'OK':
            tk.messagebox.showinfo(title='欢迎!!',message=user+'您好!')
            root.destroy()
            show_user_menu(user)
        else: 
            tk.messagebox.showinfo(message='您输入有误,请重新输入!')
    elif user[0:1] == 'l':     
        res = main1(s,user,passwd)
        if res == 'OK':
            tk.messagebox.showinfo(title='欢迎!!',message=user+'您好!')
            root.destroy()
            show_leader_menu(user)
        else: 
            tk.messagebox.showinfo(message='您输入有误,请重新输入!')
    else:
        tk.messagebox.showinfo(message='您输入有误,请重新输入!')
 
# login and sign up
btn_login = tk.Button(root, text="登录", command=usr_login)
btn_login.place(x=350, y=202)



root.mainloop()
