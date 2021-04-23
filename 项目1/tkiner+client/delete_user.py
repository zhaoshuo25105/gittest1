from tkinter import *
import tkinter.messagebox
from super_user_1 import *
from PIL import ImageTk, Image
def delete_user(root):
    root = Toplevel(root)
    root.title("admin  "+"删除用户")
    root.geometry("450x300+300+200")
    root.resizable(False, False)


    
    option = '请填写用户信息:'
    Label(root, text= option).place(x=50,y=50)
    Label(root, text="工号:").place(x=100,y=100)
    Label(root, text="密码:").place(x=100,y=150)

    var_user_id = StringVar()
    var_passwd = StringVar()

    entry_var_user_id = Entry(root, textvariable=var_user_id)
    entry_var_user_id.place(x=200, y=100)
    entry_var_passwd = Entry(root, textvariable=var_passwd)
    entry_var_passwd.place(x=200, y=150)

    def create():
        user_id = var_user_id.get()
        passwd = var_passwd.get()
        data = "#D"+"###"+user_id+"###"+passwd
        res = dropuser(s,data)
        if res == 'OK':
            tkinter.messagebox.showinfo(message='删除成功!') 
            root.destroy()
        else:
            tkinter.messagebox.showinfo(message='删除失败!') 

    Button(root,text='删除',command=create).place(x=330, y=200)

