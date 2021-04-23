from tkinter import ttk
from tkinter import *
from user_attclient import *
from PIL import ImageTk, Image
def showinfo_application_for_reimbursement():
    root = Tk()  # 初始框的声明
    root.title("报销详情")
    root.geometry("465x300+300+200")
    root.resizable(False, False)

    scrollbar = Scrollbar(root,orient=VERTICAL)#orient默认为纵向
    scrollbar.pack(fill=Y, side=RIGHT)


    
    columns = ("编号", "工号",'报销金额','报销事由','审批状态')
    treeview = ttk.Treeview(root, height=18, show="headings", columns=columns, yscrollcommand=scrollbar.set)  # 表格
    treeview.pack()

    treeview.column("编号", width=60, anchor='center') # 表示列,不显示
    treeview.column("工号", width=60, anchor='center')
    treeview.column("报销金额", width=90, anchor='center')
    treeview.column("报销事由", width=180, anchor='center')
    treeview.column("审批状态", width=60, anchor='center')


    treeview.heading("编号", text="编号") # 显示表头
    treeview.heading("工号", text="工号")
    treeview.heading("报销金额", text="报销金额")
    treeview.heading("报销事由", text="报销事由")
    treeview.heading("审批状态", text="审批状态")


    treeview.pack(side=LEFT, fill=BOTH)
    id = []
    number = []
    money = []
    reason = []
    status = []
    res = read_reim(s)
    for r in res:
        id.append(r[0])
    for r in res:
        number.append(r[1])
    for r in res:
        money.append(r[2])
    for r in res:
        reason.append(r[3])
    for r in res:
        status.append(r[4])
    
    for i in range(len(id)): # 写入数据
        treeview.insert('', i, values=(id[i],number[i],money[i],reason[i],status[i]))
   
    scrollbar.config(command=treeview.yview)
    root.mainloop()
