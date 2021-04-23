from tkinter import *
from PIL import ImageTk, Image
def show_announce():
    root = Tk()
    root.title("关于!!!")
    root.geometry("450x300+300+200")
    root.resizable(False, False)

    
    notice = '''今天发工资!! 今天休假休假休假! 发年终奖!!! 发年终奖!!! 
    发年终奖!!! 发年终奖!!! 发年终奖!!! '''
    Label(root, text= notice).place(x=50,y=100)
    root.mainloop()