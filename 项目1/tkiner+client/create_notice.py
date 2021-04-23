from tkinter import *
import tkinter.messagebox
from super_user_1 import *
from PIL import ImageTk, Image
def create_notice(root):
    root = Toplevel(root)
    root.title("admin  "+"创建公告")
    root.geometry("450x300+300+200")
    root.resizable(False, False)


    option = '请填写公告信息:'
    Label(root, text= option).place(x=50,y=50)
    Label(root, text="标题:").place(x=100,y=100)
    Label(root, text="内容:").place(x=100,y=150)


    var_dataname = StringVar()

    entry_dataname = Entry(root, textvariable=var_dataname ,width=30)
    entry_dataname.place(x=160, y=100)
    entry_data = Text(root, height=6,width=30)
    entry_data.place(x=160, y=150)
    def create():
        dataname = var_dataname.get()
        data = entry_data.get('1.0','end')
        l = [dataname,data]
        res = createsign(s,l)
        if res == 'OK':
            tkinter.messagebox.showinfo(message='创建成功!') 
            root.destroy()
        else:
            tkinter.messagebox.showinfo(message='创建失败!') 


    Button(root,text='创建',command=create).place(x=350, y=250)

