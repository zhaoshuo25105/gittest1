from tkinter import ttk
from tkinter import *
from click2 import *
from user_attclient import *
from super_user_1 import *
from PIL import ImageTk, Image
def exam_application_for_reimbursement():
    root = Tk()  # 初始框的声明
    root.title("审批报销")
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
    isreim = '1'
    res = do_auditing(s,isreim)
    if res == '无报销记录':
        messagebox.showinfo(message='暂无数据!')
        root.destroy()
    else:
        id = []
        number = []
        money = []
        reason = []
        status = []
        for r in res:
            id.append(r[0])
            number.append(r[1])
            money.append(r[2])
            reason.append(r[3])
            status.append(r[4])

        for i in range(len(id)): # 写入数据
            treeview.insert('', i, values=(id[i],number[i],money[i],reason[i],status[i]))

        def treeviewClick(event):#单击
            for item in treeview.selection():
                item_text = treeview.item(item,"values")
                root.destroy()
                showclick(item_text)
                
        treeview.bind('<ButtonRelease-1>', treeviewClick)#绑定单击离开事件===========
        scrollbar.config(command=treeview.yview)
    root.mainloop()
