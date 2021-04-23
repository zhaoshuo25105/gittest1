import tkinter
from tkinter import ttk  # 导入内部包
import tkinter.messagebox
from user_attclient import *

def showclick(item_text):
    root = tkinter.Tk()
    root.title('&&')
    root.geometry("200x100+350+250")

    def print1():
        option = '1'
        reim_id = item_text[0]
        res = do_auditing_handle(s,reim_id,option)
        if res == 'ERR':
            tkinter.messagebox.showinfo(message='审批失败!')
            root.destroy()
        elif res == 'OK1':
            tkinter.messagebox.showinfo(message='审批成功!')
            root.destroy()
    def print0():
        option = '2'
        reim_id = item_text[0]
        res = do_auditing_handle(s,reim_id,option)
        if res == 'ERR':
            tkinter.messagebox.showinfo(message='审批失败!')
            root.destroy()
        elif res == 'OK2':
            tkinter.messagebox.showinfo(message='驳回成功!')
            root.destroy()
      
    label = tkinter.Label(root,text='您是否通过:')
    label.place(x=40,y=20)
    btn_yes = tkinter.Button(root, text="是", command = print1)
    btn_yes.place(x=60,y=60)
    btn_no = tkinter.Button(root, text="否", command = print0)
    btn_no.place(x=120,y=60)
 
 

 

 
    root.mainloop()

