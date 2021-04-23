from tkinter import ttk
from tkinter import *
from click1 import *
from user_attclient import *
from PIL import ImageTk, Image
def showexamination_and_approval_leave():
    root = Tk()  # 初始框的声明
    root.title("审批请假")
    root.geometry("375x300+300+200")
    root.resizable(False, False)
    

    
    scrollbar = Scrollbar(root,orient=VERTICAL)#orient默认为纵向
    scrollbar.pack(fill=Y, side=RIGHT)
    columns = ("工号", "状态","打卡时间","备注")
    treeview = ttk.Treeview(root, height=30, show="headings", columns=columns, yscrollcommand=scrollbar.set)  # 表格
    treeview.pack()
    treeview.column("工号", width=70, anchor='center') # 表示列,不显示
    treeview.column("状态", width=60, anchor='center')
    treeview.column("打卡时间", width=170, anchor='center')
    treeview.column("备注", width=60, anchor='center')


    treeview.heading("工号", text="工号") # 显示表头
    treeview.heading("状态", text="状态")
    treeview.heading("打卡时间", text="打卡时间")
    treeview.heading("备注", text="备注")

    treeview.pack(side=LEFT, fill=BOTH)

    res = set_work(s)


    if res=='暂无数据':
        messagebox.showinfo(message='暂无数据!')
        root.destroy()
    else:
        id = []
        status = []
        time = []
        reason = []
        for r in res:
            id.append(r[0])
            reason.append(r[3])
            time.append(r[2])
        for r in res:
            if r[1] == '1':
                status.append('正常')
            else:
                status.append('异常')

            
        for i in range(len(status)): # 写入数据
            treeview.insert('', i, values=(id[i],status[i],time[i],reason[i]))

        def treeviewClick(event):#单击
            for item in treeview.selection():
                item_text = treeview.item(item,"values")
                root.destroy()
                showclick(item_text)
                
        treeview.bind('<ButtonRelease-1>', treeviewClick)#绑定单击离开事件===========
        scrollbar.config(command=treeview.yview)
  
    root.mainloop()
