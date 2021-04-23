from tkinter import *
import tkinter.messagebox
from super_user_1 import *
from PIL import ImageTk, Image
def delete_notice(root):
    root = Toplevel(root)
    root.title("admin  "+"删除公告")
    root.geometry("450x300+300+200")
    root.resizable(False, False)


    option = '请填写公告信息:'
    Label(root, text= option).place(x=50,y=50)
    Label(root, text="公告编号:").place(x=100,y=100)
    Label(root, text="公告标题:").place(x=100,y=150)

    var_data_id = StringVar()
    var_data_name = StringVar()

    entry_var_data_id = Entry(root, textvariable=var_data_id)
    entry_var_data_id.place(x=200, y=100)
    entry_var_data_name = Entry(root, textvariable=var_data_name)
    entry_var_data_name.place(x=200, y=150)

    def create():
        data_id = var_data_id.get()
        data_name = var_data_name.get()
  
        res = dropsign(s,data_id)
        if res == 'OK':
            tkinter.messagebox.showinfo(message='删除成功!') 
            root.destroy()
        else:
            tkinter.messagebox.showinfo(message='删除失败!') 

    Button(root,text='删除',command=create).place(x=330, y=200)

