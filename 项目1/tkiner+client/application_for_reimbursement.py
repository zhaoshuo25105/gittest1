import pickle  # 存放数据的模块
import tkinter as tk
from user_attclient import *
from PIL import ImageTk, Image
def show_application_for_reimbursement(root):
    def submit():
        money = var_money.get()
        reason = entry_reason.get('1.0','end')
        res = do_reim(s,money,reason)
        if res == 'OK':
            tk.messagebox.showinfo(message='申请成功!!')
            root.destroy()
        else:
            tk.messagebox.showinfo(message='失败!!')
            root.destroy()

    root = tk.Toplevel(root)
    root.title("申请报销")
    root.geometry("450x300+300+200")
    root.resizable(False, False)
    


    tk.Label(root, text='申请金额:').place(x=50, y=100)
    tk.Label(root, text='申请事由:').place(x=50, y=140)

    var_money = tk.StringVar()

    entry_money = tk.Entry(root, textvariable=var_money,width=30)
    entry_money.place(x=130, y=100)
    entry_reason = tk.Text(root, height=6,width=30)
    entry_reason.place(x=130, y=140)
    tk.Button(root, text="确认申请", command=submit).place(x=350,y=230)
