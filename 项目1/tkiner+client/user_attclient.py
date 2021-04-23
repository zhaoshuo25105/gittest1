#coding=utf-8
'''
员工自助系统
'''

from  socket import *
import time,datetime
from clientsettings import * 
import sys
import getpass
from super_user_1 import *

#创建套接字,进入一级界面
def main1(s,user,passwd):

    if user not in ('',None,' ') and passwd not in ('',None,' '):
        data = "%s##%s"%(user,passwd)
        
        s.send(data.encode())
        response = s.recv(128)
        if response == b"LOK":
            res = 'OK'
        elif response == b"NOK":
            res = 'OK'
        else:
            res = 'NO'
    else:
        res = 'NO'
    return res



def show_myself(s):
    s.send(b"R")
    response = s.recv(1000).decode()
    if response == "ERR":
        res = 'NO'
    else:
        res = response
    return res



        


# 查看考勤函数
def get_work(s):
    s.send(b'G')
    response = s.recv(128)
    if response == b'YES':
        s.send(b'1')
        res = s.recv(200).decode().split('##')
        a, b, c = res

        s.send(b'1')
        data = s.recv(1024*10).decode().split('##')
    return res + data

       




# 查看所有下属员工
def get_under_userwork_all(s,id):
    
    s.send(b'GUS')
    response = s.recv(128).decode()
    if response == 'YES':
        s.send(b'1')
        data = s.recv(1024*10)
        if data == b'FAIL':
            return '您无下属员工'
        # 接收员工数据
        data = data.decode().split('##')
        all = []
        for x in data:
            if not x:
                break
            x = eval(x)
            all.append(x)
        if id == '0':
            single = []
        else:
            s.send(id.encode())
            # 接收考勤数据
            data = s.recv(1024*10)
            if data==b'FAIL':
                return '无考勤记录'
            data = data.decode().split('##')
            single = []
            for x in data:
                if not x:
                    break
                x = eval(x)
                single.append(x)
        
        return [all,single]

def get_under_userwork_single(s,id):
    
    s.send(b'SWWI')
    response = s.recv(128).decode()
    single = []
    if response == 'YES':
        s.send(id.encode())
        # 接收考勤数据
        data = s.recv(1024*10)
        if data==b'FAIL':
            return '无考勤记录'
        data = data.decode().split('##')
        
        for x in data:
            if not x:
                break
            x = eval(x)
            single.append(x)
    return single




# 领导审批员工考勤函数
def set_work(s):
    s.send(b'SET')
    response = s.recv(128).decode()
    if response == 'YES':
        s.send(b'1')
        data = s.recv(1024*10).decode()
        if data=='ERROR':
            return '暂无数据'
        data = data.split('##')
        info = []
        for x in data:
            if x == '':
                break
            x = eval(x)
            info.append(x)

    return info

def set_single_work(s,user_id,isagree,date): 
    s.send(b'SSW')
    response = s.recv(128).decode()
    if response == 'YES':
        
        data = '%s##%s##%s'%(user_id,isagree,date)

        s.send(data.encode())
        res = s.recv(128).decode()
        if res == 'ERR':
            return 'NO'
        else:
            return 'OK'
        

# 打卡功能函数       
def do_work(s,iswork,workdesc):
    s.send(b'D')
    response = s.recv(128)
    if response == b'YES':

        if not iswork:
            s.send('EXIT##1'.encode())

        elif iswork == '4':
            s.send('EXIT##1'.encode())

        elif iswork == '1':
            data = 'WORK##'
            s.send(data.encode())

        elif iswork in ['2','3']:
            data = iswork+'##'+workdesc
            s.send(data.encode())
            
        else:
            s.send('EXIT##1'.encode())
            return 'NO'
        response = s.recv(128).decode()
        if response == 'OK':
            res = 'OK'
        elif response == 'FAIL':
            res = 'NO'
    return res


# 报销
def do_reim(s,reimmoney,reimdesc):
    s.send(b'REIM')
    response = s.recv(128).decode()
    if response == 'REIMOK':
        # 将申报金额和申报注释 与 ## 拼接成字符串发送到服务端
        data = reimmoney+'##'+reimdesc
        s.send(data.encode())

    response = s.recv(128).decode()
    if response == 'OK':
        res = 'OK'
    elif response == 'FAIL':
        res = 'NO'
    return res

# 审核报销
def do_auditing(s,isreim):
    s.send(b'AUD')
    response = s.recv(128).decode()
    if response == 'OK':
       
        # 审核所有待审核报销
        if isreim == '1':
            data = '1##AUD'
            s.send(data.encode())
           
            
            
            response = s.recv(4096).decode()
            if response == 'END':
                # 待审核报销申请全部发送完毕,或未找到待审核申请
                return '无报销记录'
            else:
                response = response.split('##')
                info = []
                for x in response:
                    if x == '':
                        break
                    x = eval(x)
                    info.append(x)
                return info



def do_auditing_handle(s,reim_id,option):       
    s.send(b'AUDH')
    response = s.recv(128).decode()
    if response == 'OK':
        data = '%s##%s'% (reim_id,option)
        s.send(data.encode())
        result = s.recv(4096).decode()
        return result
            


# 查看报销申请
def read_reim(s):
    s.send(b'READ')
    res = []
    while True:
        response = s.recv(4096).decode()
        if response == 'ENDZERO':
            return '没有记录'
        elif response == 'ENDALL':
            return res
        else:
            reim_l = response.split('##')
            res.append([reim_l[0],reim_l[1],reim_l[2],reim_l[3],reim_l[4]])
            s.send(b'GO')
        






def read_balance(s):
    s.send(b'B')
    response = s.recv(128).decode()
    if response == "ERR":
        res = "查询失败"
        return
    elif response == "Zero":
        res = "公司还没有采集您的基础信息,请尽快填写"
    else:
        # bakance 是工资  count是缺勤天数
        data = response.split('##')
        f = float(data[3])
        data[4] = float(data[4])
        data[5] = float(data[5])
        # 应发工资
        y = float(data[9])
        # y = str(round(y,2))


        # 五险一金
        # 医疗保险：个人２５００＊２％＝５０元，单位２５００＊６％＝１５０元

        yiliao = y * 0.02
        yiliao1 = y * 0.06

        # 养老保险：个人２５００＊８％＝２００元，单位２５００＊２０％＝５００元
        yanglao = y * 0.08
        yanglao1 = y * 0.2

        # 失业保险：个人２５００＊１％＝２５元，单位２５００＊２％＝５０元
        shiye = y * 0.01
        shiye1 = y * 0.02

        # 工伤保险：个人无，单位２５００＊０．６％＝１５元，或２５００＊１．２％＝３０元，或２５００＊２％＝５０元
        gongshang1 = y * 0.06

        # 生育保险：个人无，单位２５００＊１％＝２５元
        shengyu = y * 0.01

        geren = yiliao + yanglao + shiye
        gongsi = yiliao1 + yanglao1 + shiye1 + gongshang1 + shengyu
        # 实发工资
        shifa = y - geren
        if data[4] == 0:
            man = 200
        else:
            man = 0
        
        y = str(round(y, 2))
        geren = str(round(geren, 2))
        shifa = str(round(shifa, 2))
        # 工资
        f = str(round(f, 2))
        data[4] = str(round(data[4], 2))
        data[5] = str(round(data[5], 2))
        man = str(round(man, 2))

        res = (data[0], \
                data[2], f, data[4],\
                data[5], man, data[7],\
                data[6], data[8], y, geren, shifa)
    return res


# 查询公告的函数
def show_notice_client(s):
    # 调用此函数,发送se到客户端
    s.send(b'SE')
    response = s.recv(128).decode()
    # 判断是否连接
    if response == 'ok':

        s.send('1'.encode())


    noticefile = s.recv(4096).decode()
    if noticefile == 'null':
        res = '暂无公告!!!'
    else:
        noticefile1 = noticefile.split('##')
        res = []
        for x in noticefile1:
            if x == '':
                break
            x = eval(x)              

            res.append(x)
    return res

