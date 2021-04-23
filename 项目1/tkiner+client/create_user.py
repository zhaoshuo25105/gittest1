from tkinter import *
import tkinter.messagebox
from super_user_1 import *
from PIL import ImageTk, Image
def creat_user(root):
    root = Toplevel(root)
    root.title("admin  "+"创建用户")
    root.geometry("450x500+300+200")
    root.resizable(False, False)

    
    option = '请填写用户信息:'
    Label(root, text= option).place(x=50,y=50)
    Label(root, text="工号:").place(x=100,y=100)
    Label(root, text="密码:").place(x=100,y=150)
    Label(root, text="姓名:").place(x=100,y=200)
    Label(root, text="手机号:").place(x=100,y=250)
    Label(root, text="部门编号:").place(x=100,y=300)
    Label(root, text="薪资标准:").place(x=100,y=350)

    var_user_id = StringVar()
    var_passwd = StringVar()
    var_user_name = StringVar()
    var_user_phone = StringVar()
    var_pro_no = StringVar()
    var_balance_flag = StringVar()

    entry_var_user_id = Entry(root, textvariable=var_user_id)
    entry_var_user_id.place(x=200, y=100)
    entry_var_passwd = Entry(root, textvariable=var_passwd)
    entry_var_passwd.place(x=200, y=150)
    entry_var_user_name = Entry(root, textvariable=var_user_name)
    entry_var_user_name.place(x=200, y=200)
    entry_var_user_phone = Entry(root, textvariable=var_user_phone)
    entry_var_user_phone.place(x=200, y=250)
    entry_var_pro_no = Entry(root, textvariable=var_pro_no)
    entry_var_pro_no.place(x=200, y=300)
    entry_var_balance_flag = Entry(root, textvariable=var_balance_flag)
    entry_var_balance_flag.place(x=200, y=350)
    def create():
        user_id = var_user_id.get()
        passwd = var_passwd.get()
        user_name = var_user_name.get()
        user_phone = var_user_phone.get()
        pro_no = var_pro_no.get()
        balance_flag = var_balance_flag.get() 
        data = "#C"+"###"+user_id+"###"+passwd+"###"+user_name+"###"+user_phone+\
    "###"+pro_no+"###"+balance_flag
        res = createuser(s,data)
        if res == 'OK':
            tkinter.messagebox.showinfo(message='创建成功!') 
            root.destroy()
        else:
            tkinter.messagebox.showinfo(message='创建失败!') 

    Button(root,text='创建',command=create).place(x=330, y=400)

