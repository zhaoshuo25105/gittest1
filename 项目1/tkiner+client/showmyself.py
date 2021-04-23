from tkinter import ttk
from tkinter import *
from user_attclient import *
from PIL import ImageTk, Image
def showmyself():
    root = Tk()  # 初始框的声明
    root.title("myself")
    root.geometry("450x300+300+200")
    root.resizable(False, False)

    
    columns = ("  ", "       ")
    treeview = ttk.Treeview(root, height=18, show="headings", columns=columns)  # 表格
    
    treeview.column("  ", width=150, anchor='center') # 表示列,不显示
    treeview.column("       ", width=300, anchor='center')
    
    treeview.heading("  ", text="  ") # 显示表头
    treeview.heading("       ", text="       ")
    
    treeview.pack(side=LEFT, fill=BOTH)
    res = show_myself(s)
    name = ['工号','姓名','电话号','部门编号','薪资']
    ipcode = res.split('##')
    for i in range(min(len(name),len(ipcode))): # 写入数据
        treeview.insert('', i, values=(name[i], ipcode[i]))
    root.mainloop()
