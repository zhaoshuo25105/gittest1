
from tkinter import *
from showmyself import *
from showoption import *
from check_work import *
from show_salary import *
from application_for_reimbursement import *
from info_application_for_reimbursement import *
from shownotice import *
from show_announce import *
from PIL import ImageTk, Image
def show_user_menu(usr_name):
    root = Tk()
    root.title(usr_name+"欢迎回家")
    root.geometry("450x300+300+200")
    root.resizable(False, False)

    canvas = Canvas(root, width=450,height=300,bd=0, highlightthickness=0)
    imgpath = '3.gif'
    img = Image.open(imgpath)
    photo = ImageTk.PhotoImage(img)
    
    canvas.create_image(0, 0, anchor='nw',image=photo)
    canvas.pack()
    
    def hello():
        print("hello!")

    menubar = Menu(root)
 
    # create a pulldown menu, and add it to the menu bar
    filemenu = Menu(menubar, tearoff=0)
    showclock_son_menu = Menu(filemenu,tearoff=0)
    reimbursement_son_menu = Menu(filemenu,tearoff=0)
    filemenu.add_command(label="myself", command=showmyself)

    filemenu.add_cascade(label="打卡", menu=showclock_son_menu)
    showclock_son_menu.add_command(label="操作详情", command=lambda :showoption(root))
    showclock_son_menu.add_command(label="查看记录", command=showcheck_work_info)

    filemenu.add_command(label="工资", command=show_salary)
    filemenu.add_command(label="考勤", command=showcheck_work)

    filemenu.add_cascade(label="报销", menu=reimbursement_son_menu)
    reimbursement_son_menu.add_command(label="申请报销", command=lambda :show_application_for_reimbursement(root))
    reimbursement_son_menu.add_command(label="查看报销", command=showinfo_application_for_reimbursement)

    filemenu.add_command(label="查看公告", command=show_notice)
    filemenu.add_separator()
    filemenu.add_command(label="退出", command=root.destroy)
    menubar.add_cascade(label="菜单", menu=filemenu)


    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="关于", command=show_announce)
    menubar.add_cascade(label="帮助", menu=helpmenu)

    # display the menu
    root.config(menu=menubar)
    root.mainloop()