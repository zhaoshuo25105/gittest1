from tkinter import ttk
from tkinter import *
from check_work_info import *
from user_attclient import * 
from PIL import ImageTk, Image
def showcheck_work():
    root = Tk()  # 初始框的声明
    root.title("我的考勤")
    root.geometry("450x300+300+200")
    root.resizable(False, False)

 
    
    columns = ("myself", "天数&")
    treeview = ttk.Treeview(root, height=18, show="headings", columns=columns)  # 表格

    treeview.column("myself", width=150, anchor='center') # 表示列,不显示
    treeview.column("天数&", width=300, anchor='center')

    treeview.heading("myself", text="myself") # 显示表头
    treeview.heading("天数&", text="天数&")

    treeview.pack(side=LEFT, fill=BOTH)

    name = ['本月所需考勤','正常出勤','异常出勤']
    res = get_work(s)
    ipcode = [res[0],res[1],res[2]]
    for i in range(min(len(name),len(ipcode))): # 写入数据
        treeview.insert('', i, values=(name[i], ipcode[i]))

    Button(root, text="考勤详情", command = showcheck_work_info).place(x=90,y=100)
    root.mainloop()
