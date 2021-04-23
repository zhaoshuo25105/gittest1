from tkinter import ttk
from tkinter import *
from user_attclient import *
from PIL import ImageTk, Image
def showcheck_work_info():
    root = Tk()  # 初始框的声明
    root.title("考勤详情")
    root.geometry("465x300+300+200")
    root.resizable(False, False)

    
    scrollbar = Scrollbar(root,orient=VERTICAL)#orient默认为纵向
    scrollbar.pack(fill=Y, side=RIGHT)
    columns = ("工号", "状态","打卡时间","备注","审批意见")
    treeview = ttk.Treeview(root, height=18, show="headings", columns=columns, yscrollcommand=scrollbar.set)  # 表格
    treeview.pack()

    treeview.column("工号", width=70, anchor='center') # 表示列,不显示
    treeview.column("状态", width=60, anchor='center')
    treeview.column("打卡时间", width=170, anchor='center')
    treeview.column("备注", width=60, anchor='center')
    treeview.column("审批意见", width=90, anchor='center')


    treeview.heading("工号", text="工号") # 显示表头
    treeview.heading("状态", text="状态")
    treeview.heading("打卡时间", text="打卡时间")
    treeview.heading("备注", text="备注")
    treeview.heading("审批意见", text="审批意见")

    treeview.pack(side=LEFT, fill=BOTH)
    res = get_work(s)
    id = eval(res[3])[0]
    status = []
    time = []
    reason = []
    exam = []
    for x in range(3,len(res)-1):
        r = eval(res[x])
        if r[1] == '1':
            status.append('正常')
        else:
            status.append('异常')
    for x in range(3,len(res)-1):
        r = eval(res[x])
        time.append(r[2])
    for x in range(3,len(res)-1):
        r = eval(res[x])
        reason.append(r[3])
    for x in range(3,len(res)-1):
        r = eval(res[x])
        if r[4] == '0':
            exam.append('未审批')
        elif r[4] == '1':
            exam.append('已审批')
        elif r[4] == '2':
            exam.append('驳回')
        else:
            exam.append('正常')
        
    for i in range(len(status)): # 写入数据
        treeview.insert('', i, values=(id,status[i],time[i],reason[i],exam[i]))

    scrollbar.config(command=treeview.yview)
    root.mainloop()
