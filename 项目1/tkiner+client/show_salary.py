from tkinter import *
from user_attclient import *
from PIL import ImageTk, Image
def show_salary():
    root = Tk()
    root.title("薪酬！!")
    root.geometry("450x300+300+200")
    root.resizable(False, False)
    res = read_balance(s)
   

    
    info = '''%s 您好!! 您的基本工资为 %s 元,
    考勤所得工资为 %s 元,
    缺勤天数 %s，扣除工资 %s ,
    满勤奖 %s ,旷工天数 %s ,请假总天数%s ,
    年假 %s,应发 %s,五险一金 %s,实发 %s !!!!
    希望您再接再厉,丰富自己,努力为公司再创佳绩!! 辛苦啦!''' % res
    

    Label(root, text= info).place(x=50,y=100)
    root.mainloop()