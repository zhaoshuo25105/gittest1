from tkinter import *
from user_attclient import *
from PIL import ImageTk, Image
def showoption(root):
    def submit():
        option = var_option.get()
        reason = var_reason.get()
        res = do_work(s,option,reason)
        if res == 'OK':
            if option == '1':
                messagebox.showinfo(message='打卡成功!')
            elif option == '2':
                messagebox.showinfo(message='请假成功!')
            elif option == '3':
                messagebox.showinfo(message='请假成功!')
        else:
            messagebox.showinfo(message='失败!')
        root1.destroy()

    root1 = Toplevel(root)  # 初始框的声明
    root1.title("option")
    root1.geometry("450x300+300+200")
    root1.resizable(False, False)

 

    option = '请选择您的操作:'
    Label(root1, text= option).place(x=50,y=50)
    Label(root1, text="1.打卡").place(x=100,y=100)
    Label(root1, text="2.事假").place(x=150,y=100)
    Label(root1, text="3.年假").place(x=200,y=100)

    Label(root1, text="您的选择是:").place(x=80,y=150)
    Label(root1, text="备注:").place(x=80,y=190) 

    var_option = StringVar()
    var_reason = StringVar()

    entry_option = Entry(root1, textvariable=var_option)
    entry_option.place(x=160, y=150)
    entry_reason = Entry(root1, textvariable=var_reason)
    entry_reason.place(x=160, y=190)

    
    Button(root1,text='提交',command=submit).place(x=350,y=220)


