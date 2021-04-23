from tkinter import ttk
from tkinter import *
from check_work import *
from check_work_info_single import *
from PIL import ImageTk, Image
def showworker_work():
    root = Tk()  # 初始框的声明
    root.title("查看员工")
    root.geometry("465x300+300+200")
    root.resizable(False, False)


    
    scrollbar = Scrollbar(root,orient=VERTICAL)#orient默认为纵向
    scrollbar.pack(fill=Y, side=RIGHT)

    columns = ("工号","姓名","电话")
    treeview = ttk.Treeview(root, height=18, show="headings", columns=columns, yscrollcommand=scrollbar.set)  # 表格
    treeview.pack()

    treeview.column("工号", width=110, anchor='center') # 表示列,不显示
    treeview.column("姓名", width=170, anchor='center')
    treeview.column("电话", width=170, anchor='center')


    treeview.heading("工号", text="工号") # 显示表头
    treeview.heading("姓名", text="姓名")
    treeview.heading("电话", text="电话")

    treeview.pack(side=LEFT, fill=BOTH)
    id = '0'
    res = get_under_userwork_all(s,id)
    if res == '您无下属员工':
        messagebox.showinfo(message='您无下属员工!')
        root.destroy()
    else:
        id = []
        names = []
        phones = []
        for r in res[0]:
            id.append(r[0])
            names.append(r[1])
            phones.append(r[2])

        for i in range(len(names)): # 写入数据
            treeview.insert('', i, values=(id[i],names[i],phones[i]))
        def treeviewClick(event):#单击
            for item in treeview.selection():
                item_text = treeview.item(item,"values")
                id = item_text[0]
                res = get_under_userwork_single(s,id)
                showcheck_work_info_single(res)
                    
             
        
    try:
        treeview.bind('<ButtonRelease-1>', treeviewClick)#绑定单击离开事件===========

        scrollbar.config(command=treeview.yview)
    except Exception:
        pass
    root.mainloop()
