from create_user import *
from delete_user import *
from tkinter import *
from create_notice import *
from delete_notice import *
from show_announce import *
from PIL import ImageTk, Image
def show_superuser_menu(user):
    root = Tk()
    root.title(user+"欢迎回家")
    root.geometry("450x300+300+200")
    root.resizable(False, False)

    canvas = Canvas(root, width=450,height=300,bd=0, highlightthickness=0)
    imgpath = '3.gif'
    img = Image.open(imgpath)
    photo = ImageTk.PhotoImage(img)
    
    canvas.create_image(0, 0, anchor='nw',image=photo)
    canvas.pack()
    

    menubar = Menu(root)

    # create a pulldown menu, and add it to the menu bar
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="创建用户", command=lambda :creat_user(root))
    filemenu.add_command(label="删除用户", command=lambda :delete_user(root))
    filemenu.add_command(label="添加公告", command=lambda :create_notice(root))
    filemenu.add_command(label="删除公告", command=lambda :delete_notice(root))
    filemenu.add_separator()
    filemenu.add_command(label="退出", command=root.destroy)
    menubar.add_cascade(label="菜单", menu=filemenu)




    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="关于", command=show_announce)
    menubar.add_cascade(label="帮助", menu=helpmenu)

    # display the menu
    root.config(menu=menubar)
    root.mainloop()
