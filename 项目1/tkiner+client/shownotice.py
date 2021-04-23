from tkinter import *
from user_attclient import *
from PIL import ImageTk, Image
def show_notice():
    root = Tk()
    root.title("公告!!!")
    root.resizable(False, False)
    root.geometry("450x300+300+200")


    
    Label(root, text="公告",font= "Fixdsys 25").place(x=190,y=30)
    res = show_notice_client(s)
    if res == '暂无公告!!!':
        root.destroy()
        messagebox.showinfo(message='暂无公告!')
    else:
        notice = ''
        for r in res:
            notice = notice + '标题：%s' % r[1] + '\n' \
                + '时间: %s' % r[3] + '\n' + '内容: %s' % r[2] + '\n'
        

        Label(root, text= notice).place(x=70,y=80)


    root.mainloop()