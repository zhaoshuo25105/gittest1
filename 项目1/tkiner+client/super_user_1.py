#coding=utf-8
'''
员工自助系统超级用户
'''

from  socket import *
import time
from clientsettings import * 
import sys
import getpass

s = socket()

#创建套接字,进入一级界面
def main(s,user,passwd):
    if user not in ('',None,' ') and passwd not in ('',None,' '):
        data = "%s##%s"%(user,passwd)
        s.send(data.encode())
        response = s.recv(128)
        if response == b"OK":
            res = 'OK'
        else:
            res = 'NO'
    else:
        res = 'NO'
    return res

    


#创建新用户
def createuser(s,data):
    s.send(data.encode())
    response1 = s.recv(128).decode()
    if response1 == "OK": 
        res = 'OK'
    else:
        res = 'NO'
    return res
#删除用户函数   
def dropuser(s,data):
    s.send(data.encode())
    response1 = s.recv(128).decode()
    if response1 == "OK":
        res = 'OK'
    else:
        res = 'NO'
    return res

#创建新公告
def createsign(s,l):
 
    s.send(b"#S")
    flag = s.recv(128).decode()
    if flag == "OK":
        s.send(l[0].encode())
        response = s.recv(128).decode()
        if response == 'OK':
            s.send(l[1].encode())
            s.send(b"##")
            time.sleep(3)
            response = s.recv(128).decode()
    if response == "SURE":
        res = 'OK'
    else:
        res = 'NO'
    return res

#根据id删除公告       
def dropsign(s,data):
    s.send(("#I###"+data).encode())
    response = s.recv(128).decode()
    if response == "SURE":
        res = 'OK'
    else:
        res = 'NO'
    return res
