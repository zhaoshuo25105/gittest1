# coding=utf-8
'''
员工自助系统
'''

from  socket import *
import os
import time
import sys
#配置文件settings.py
from settings import * 
import signal
import pymysql


#服务端类
class Userver(object):
    #自定义函数,参数为服务器地址
    def __init__(self,address):
        self.address = address
        self.create_socket()
        self.bind(address)

    #创建套接字
    def create_socket(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    
    #绑定地址端口
    def bind(self,address):
        self.ip = address[0]
        self.port = address[1]
        self.sockfd.bind(address)

    #监听等待连接,使用多进程,创建二级子进程处理请求
    def start_server(self):
        self.sockfd.listen(5)
        signal.signal(signal.SIGCHLD,signal.SIG_IGN)
        #此处没有设置daemon
        print("Listening from %d" % self.port)
        #连接数据库
        self.db = pymysql.connect(database_host,user,passwd,database,charset="utf8")
        while True:
            connfd,address = self.sockfd.accept()
            pid = os.fork()
            if pid < 0:
                continue
            elif pid == 0:
                self.sockfd.close()
                self.handlefirst(connfd)
                connfd.close()
                sys.exit(0)
            else:
                connfd.close()

    #客户端连接后接收账号密码并查询数据库user_passwd表对比,分出两种用户给出不同返回值
    def handlefirst(self,connfd):
        while True:
            data = connfd.recv(128).decode()
            if not data:
                break
            cursor = self.db.cursor()
            user,passwd = data.split('##')
#---------------------超级用户创建新员工-----------------------
            if user  == '1q2w3e' and passwd == "1q2w3e":
                self.supercreate(connfd,cursor)
                cursor.close()
                return
#-----------------------------------------------------------
            sql = "select substr(user_id,1,1) from user_passwd where user_id = '%s' and passwd = '%s'"%(user,passwd)
            try:
                cursor.execute(sql)
            except Exception:
                connfd.send(b"ERR")
                cursor.close()
                return
            r = cursor.fetchall()
            if len(r) != 0 and r[0][0] =="l":
                connfd.send(b"LOK")
                self.leadermenu(connfd,user,cursor)
                cursor.close()
                return
            elif len(r) != 0 and r[0][0] =="n":
                connfd.send(b"NOK")
                self.normalmenu(connfd,user,cursor)
                cursor.close()
                return
            else:
                connfd.send(b"Failed")
                cursor.close()
#================调用分支函数==============================   
    #领导函数调用菜单
    def leadermenu(self,connfd,user,cursor):
        while True: #在循环中接收客户端不同请求调用不同方法
            choose = connfd.recv(128)
            if not choose:
                pass
            elif choose == b'R':
                self.readmyself(connfd,user,cursor)
            elif choose == b'B':
                self.readbalance(connfd,user,cursor)
            elif choose == b'D':
                self.do_iswork(connfd,user,cursor)
            elif choose == b'REIM': # 领导申请报销
                self.do_reim(connfd,user,cursor)
            elif choose == b'AUD': # 领导查询员工报销
                self.do_auditing(connfd,user,cursor)
            elif choose == b'AUDH': # 审核报销
                self.do_auditing_handle(connfd,cursor) 
            elif choose == b'READ': # 领导查看报销申请
                self.read_reim(connfd,user,cursor)
            elif choose == b'G':
                self.get_work(connfd,user,cursor)
            elif choose == b'GAW':
                self.get_appoint_works(connfd,user,cursor)
            elif choose == b'GUS':
                self.get_under_userwork(connfd,user,cursor)
            elif choose == b'SWWI':
                self.select_worker_work_info(connfd,id,cursor)
            elif choose == b'SET':
                self.set_work(connfd,user,cursor)
            elif choose == b'SSW':
                self.set_single_work(connfd,cursor)
            # 领导查看公告
            elif choose == b'SE':
                self.select_notice(connfd,user,cursor)
            elif choose == b"#":
                return
            
    
    



    #普通用户调用菜单
    def normalmenu(self,connfd,user,cursor):
        while True:
            choose = connfd.recv(128)
            if not choose:
                return
            elif choose == b'R':
                self.readmyself(connfd,user,cursor)
            elif choose == b'B':
                self.readbalance(connfd,user,cursor)
            elif choose == b'D':
                self.do_iswork(connfd,user,cursor)
            elif choose == b'REIM':
                self.do_reim(connfd,user,cursor)
            elif choose == b'READ': # 员工查看报销申请
                self.read_reim(connfd,user,cursor)
            elif choose == b'G':
                self.get_work(connfd,user,cursor)
            elif choose == b'GAW':
                self.get_appoint_works(connfd,user,cursor)
            # 员工查看公告
            # 接收到se,调用查询函数
            elif choose == b'SE':
                self.select_notice(connfd,user,cursor)
            elif choose == b"#":
                return
#================================================================

    #查看自己基础信息函数
    def readmyself(self,connfd,user,cursor):
        sql = "select * from user_info where user_id = '%s';" % user
        try:
            cursor.execute(sql)
        except Exception:
            connfd.send(b"ERR")
        else:
            r = cursor.fetchall()
            if len(r) == 0:
                connfd.send(b"Zero")
            else:
                data = ''
                index = 0
                for i in r[0]:
                    if index == 0:
                        data += str(i) +'##'
                    elif index == 1:
                        data += str(i) +'##'
                    elif index == 2:
                        data += str(i) +'##'
                    elif index == 3:
                        data += str(i) +'##'
                    elif index == 4:
                        data += str(i) +'##'
                    index += 1
                connfd.send(data.encode())






    ##赵智祥
    # 查看本月工资单函数 seft connfd  员工工号 cursor
    def readbalance(self, connfd, user, cursor):
        sql = "select count(1),day(last_day(now())),\
        workdaynum(concat(substr(now(),1,8),'01'),last_day(now())) from \
        (select *  from userwork where user_id = '%s' and substr(worktime,1,7) = \
        substr(now(),1,7) and iswork = '1') A \
        join (select substr(worktime,1,10) worktime,max(worktime) \
        maxtime from userwork where user_id = '%s' group by substr(worktime,1,10)) B \
        where  A.worktime = B.maxtime;" % (user, user)
        try:
            cursor.execute(sql)
        except Exception:
            # connfd.send(b"ERR")
            return
        else:
            # r1是元祖( r[0][0]出勤天数, r[0][1]当月天数,  r[0][2]工作日天数)
            r1 = cursor.fetchall()
            if len(r1) == 0:
                # connfd.send(b"Zero")
                return
            else:
                # 查询底薪是多少                                                    员工工号
                sql = "select balance_flag from user_info where user_id = '%s';" % user
                try:
                    cursor.execute(sql)
                except Exception:
                    # connfd.send(b"ERR")
                    return
                else:
                    # 3.查询底薪的一条数据
                    r2 = cursor.fetchall()
                    if len(r2) == 0:
                        # connfd.send(b"Zero")
                        return
                    else:
                        # 工资
                        data1 = str(int(r2[0][0]) * int(r1[0][0]) / int(r1[0][2]))
                        # 4.缺勤天数
                        data2 = str(int(r1[0][2]) - int(r1[0][0]))
                        # data = data1+'##'+data2

                        # connfd.send(data.encode())

                # 1.查询姓名
                sql = "select user_name from user_info where user_id='%s';" % user
                cursor.execute(sql)
                r3 = cursor.fetchall()[0][0]
                # 2.查询工号
                # user

                # 6.请假的总天数
                sql = "select count(*) from \
                (select * from userwork where substr(worktime,1,7)\
                = substr(now(),1,7)) A join (select substr(worktime,1,10)\
                worktime,max(worktime) maxtime from userwork \
                where user_id = '%s' and substr(worktime,1,7) = substr(now(),1,7)\
                group by substr(worktime,1,10)) B \
                where A.worktime = B.maxtime and (iswork='2' or iswork='3') and A.isagree='1'\
                and A.user_id='%s';" % (user, user)
                cursor.execute(sql)
                r4 = cursor.fetchall()[0][0]


                # 7.查询年假的天数 同意的数量
                sql = "select count(*) from (select * from userwork where substr(worktime,1,7)\
                = substr(now(),1,7)) A join (select substr(worktime,1,10) worktime,max(worktime)\
                maxtime from userwork where user_id = '%s' and substr(worktime,1,7) =\
                substr(now(),1,7) group by substr(worktime,1,10)) B where A.worktime =\
                B.maxtime and (iswork='3'and isagree='1');" % user
                # isagree可以改动现在是测试要改为１
                cursor.execute(sql)
                r5 = cursor.fetchall()[0][0]

                # 年假工资
                n5 = r5 * r2[0][0] / 21


                # 8.旷工天数

                sql = "select count(*) from (select * from userwork where substr(worktime,1,7)\
                = substr(now(),1,7)) A join (select substr(worktime,1,10) worktime,max(worktime)\
                maxtime from userwork where user_id = '%s' and substr(worktime,1,7) =\
                substr(now(),1,7) group by substr(worktime,1,10)) B where A.worktime =\
                B.maxtime and (iswork='2' or iswork='3') and A.isagree='2';" % user
                cursor.execute(sql)
                r6 = cursor.fetchall()[0][0]
                # 旷工扣除的工资
                r7 = r6 * 3 * r2[0][0] / 21

                # 9.事假扣除工资
                sql = "select count(*) from (select * from userwork where substr(worktime,1,7)\
                = substr(now(),1,7)) A join (select substr(worktime,1,10) worktime,max(worktime)\
                maxtime from userwork where user_id = '%s' and substr(worktime,1,7) =\
                substr(now(),1,7) group by substr(worktime,1,10)) B where A.worktime =\
                B.maxtime and  iswork='3' and A.isagree='1';" % user
                cursor.execute(sql)
                shi = cursor.fetchall()[0][0]
                r8 = shi * r2[0][0] / 21

                # 10.总共扣除工资
                r9 = r7 + r8

                # 应发工资
                # 工资－扣除工资＋满勤奖＋年假工资
                if data2 == 0:
                    r10 = float(data1) - r9 + 200 + n5
                else:
                    r10 = float(data1) - r9 + n5
                data = str(r3) + "##" + user + "##" + str(r2[0][0]) + "##" + data1 + \
                       "##" + data2 + "##" + str(r9) + "##" + str(r4) + "##"+ str(r6) + '##' + str(r5) + "##" + str(r10)
                connfd.send(data.encode())

  
#范立勇

    # 查看考勤函数
    def get_work(self,connfd,user,cursor):
        '''
            领导和普通员工,都可以通过此函数查看自己当月的考勤记录
        '''
        connfd.send(b'YES')
        # 每月打卡的总次数,取到 每天打卡时间最新时间的一次,作为当天打卡次数
        sql = '''
            select A.* from (select * from userwork where substr(worktime,1,7) = substr(now(),1,7)) A
            join 
            (select substr(worktime,1,10) worktime,max(worktime) maxtime from userwork where user_id = '%s' and substr(worktime,1,7) = substr(now(),1,7) group by substr(worktime,1,10)) B
            where  A.worktime = B.maxtime and A.user_id='%s';''' % (user,user)
        # 获取每月 正常打卡的次数
        sql1 = '''
            select A.* from (select * from userwork where substr(worktime,1,7) = substr(now(),1,7) and iswork='1') A
            join 
            (select substr(worktime,1,10) worktime,max(worktime) maxtime from userwork where user_id = '%s' and substr(worktime,1,7) = substr(now(),1,7)  group by substr(worktime,1,10)) B
            on  A.worktime = B.maxtime and A.user_id='%s';''' % (user,user)
        # 获取每月 请假打卡的次数
        sql2 = '''
            select A.* from (select * from userwork where substr(worktime,1,7) = substr(now(),1,7)) A
            join
            (select substr(worktime,1,10) worktime,max(worktime) maxtime from userwork where user_id = '%s' and substr(worktime,1,7) = substr(now(),1,7) group by substr(worktime,1,10)) B
            where A.worktime = B.maxtime and (iswork='2' or iswork='3') and A.user_id='%s';''' % (user,user)
        try:
            # 本月打卡总次数
            sum_num = cursor.execute(sql)
        except Exception:
            return
        data1 = cursor.fetchall()
        try:
            # 正常打卡次数
            work_num = cursor.execute(sql1)
        except Exception:
            return
        try:
            # 本月请假次数,包括(年假/其他假期)
            desc_num = cursor.execute(sql2)
        except Exception:
            return
        data = "%s##%s##%s"%(sum_num, work_num, desc_num)
        res1 = connfd.recv(128)
        if res1 == b'1':
            connfd.send(data.encode())
        # 获取当月打卡记录
        content = ''
        for x in data1:
            content += x.__str__() + '##'
        res2 = connfd.recv(128)
        if res2 == b'1':
            connfd.send(content.encode())

    # 查看指定月份考勤
    def get_appoint_works(self,connfd,user,cursor):
        '''
            领导和普通员工,都可以通过此函数查看自己指定月份的考勤记录
        '''
        connfd.send(b'YES')
        year = connfd.recv(128).decode()
        if year == '#':
            return
        # 每月打卡的总次数,取到每天打卡时间最新时间的一次,作为当天打卡次数
        sql = '''
            select A.* from (select * from userwork where substr(worktime,1,7) = '%s') A
            join 
            (select substr(worktime,1,10) worktime,max(worktime) maxtime from userwork where user_id = '%s' and substr(worktime,1,7) = '%s' group by substr(worktime,1,10)) B
            where  A.worktime = B.maxtime and A.user_id='%s';''' % (year, user, year, user)
        # 获取每月 正常打卡的次数
        sql1 = '''
            select A.* from (select * from userwork where substr(worktime,1,7) = '%s') A
            join 
            (select substr(worktime,1,10) worktime,max(worktime) maxtime from userwork where user_id = '%s' and substr(worktime,1,7) = '%s' and iswork='1' group by substr(worktime,1,10)) B
            on  A.worktime = B.maxtime and A.user_id='%s';''' % (year, user, year, user)
        # 获取每月 请假打卡的次数
        sql2 = '''
            select A.* from (select * from userwork where substr(worktime,1,7) = '%s') A
            join
            (select substr(worktime,1,10) worktime,max(worktime) maxtime from userwork where user_id = '%s' and substr(worktime,1,7) = '%s' group by substr(worktime,1,10)) B
            where A.worktime = B.maxtime and (iswork='2' or iswork='3') and A.user_id='%s';''' % (year, user, year, user)
        try:
            # 打卡总次数
            sum_num = cursor.execute(sql)
            result = cursor.fetchall()
        except Exception:
            return
        try:
            # 正常打卡次数
            work_num = cursor.execute(sql1)
        except Exception:
            return
        try:
            # 请假次数,包括(年假/其他假期)
            desc_num = cursor.execute(sql2)
        except Exception:
            return
        data = "%s##%s##%s" % (sum_num, work_num, desc_num)
        connfd.send(data.encode())
        # 获取当月打卡记录
        res = connfd.recv(128)
        if res == b'1':
            content = ''
            if not result:
                connfd.send(b'FAIL')
            else:
                for x in result:
                    content += x.__str__() + '##'
                connfd.send(content.encode())

    # 领导查看下属员工考勤函数
     # 领导查看下属员工考勤函数
    # 领导查看下属员工考勤函数
    def get_under_userwork(self,connfd,user,cursor):
        '''
            不同部门领导,都可以各自通过此函数查看本部门所有员工考勤记录
        '''
        connfd.send(b'YES')
        num = connfd.recv(128)
        if num == b'1':
            sql = '''
            select * from user_info where user_id in 
            (select distinct user_id from user_info where pro_no =
            (select pro_no from user_info where user_id = '%s')
                          and user_id like 'n%%')'''%user
            try:
                cursor.execute(sql)
            except Exception:
                connfd.send(b'FAIL')
                return
            res = cursor.fetchall()
            if res:
                content = ''
                for x in res:
                    content += x.__str__() + '##'
                connfd.send(content.encode())
            else:
                connfd.send(b'FAIL')
    def select_worker_work_info(self,connfd,id,cursor):
        connfd.send(b'YES')
        id = connfd.recv(128).decode()
        if id:
            sql = '''
                select A.* from (select * from userwork where user_id='%s') A
                join
                (select user_id,substr(worktime,1,10) worktime,max(worktime) maxtime from userwork where user_id='%s' group by substr(worktime,1,10)) B
                where A.worktime = B.maxtime and A.user_id = B.user_id and A.iswork in ('1','2','3'); '''%(id,id)
            try:
                cursor.execute(sql)
            except Exception:
                connfd.send(b'FAIL')
                return
            res = cursor.fetchall()
            if res:
                content = ''
                for x in res:
                    content += x.__str__() + '##'
                connfd.send(content.encode())
            else:
                connfd.send(b'FAIL')

    # 领导审批员工考勤函数
    def set_work(self,connfd,user,cursor):
        '''
            不同部门领导,都可以各自通过此函数审批本部门员工考勤,并返回审批结果
        '''
        connfd.send(b'YES')
        sql1 = '''
            select A.user_id,A.iswork,A.worktime,A.workdesc,A.isagree from
            (select * from userwork where user_id in (select distinct user_id from user_info where pro_no =(select pro_no from user_info where user_id = '%s'))) A
            join
            (select user_id,substr(worktime,1,10) worktime,max(worktime) maxtime from userwork where user_id in (select distinct user_id from user_info where pro_no =(select pro_no from user_info where user_id = '%s')) group by user_id,substr(worktime,1,10)) B
            where A.worktime = B.maxtime and A.user_id = B.user_id and A.iswork in ('2','3') and A.isagree='0';'''%(user,user)
        try:
            cursor.execute(sql1)
        except Exception:
            connfd.send(b'ERROR')
            return
        data = cursor.fetchall()
        if len(data) == 0:
            connfd.send(b'ERROR')
            return
        content = ''
        for x in data:
            content += x.__str__() + '##'
        res = connfd.recv(128)
        if res == b'1':
            connfd.send(content.encode())




    def set_single_work(self,connfd,cursor):
        connfd.send(b'YES')
        response1 = connfd.recv(128).decode()
        
        data = response1.split('##')
            # 修改指定员工,某一天的审批状态
        sql3 = "update userwork set isagree='%s' where user_id='%s' and substr(worktime,1,10)='%s'"%(data[1],data[0],data[2][0:10])
        try:
            status = cursor.execute(sql3)
            self.db.commit()
        except Exception:
            connfd.send(b'ERR')
            self.db.rollback()
        if status:
            connfd.send(b'OK')
        else:
            connfd.send(b'ERR')
    # 打卡功能函数
    def do_iswork(self,connfd,user,cursor):
        '''
            员工打卡函数,将员工打卡状态插入到数据库的员工出勤表,并返回打卡结果
        '''
        user_id = user
        connfd.send(b'YES')
        response = connfd.recv(128).decode()
        data,workdesc =  response.split('##')
        if data =='EXIT':
            return
        elif data in ['2','3']:
            iswork = data
            sql = "insert into userwork(worktime, user_id, iswork, workdesc, isagree)values (now(), '%s', '%s', '%s', '0');" % (user_id, iswork, workdesc)
        elif data == 'WORK':
            iswork = '1'
            sql = "insert into userwork(user_id, iswork, worktime, workdesc, isagree)values ('%s','%s', now(),'SUCCESS','2');" % (user_id, iswork)
        try:
            cursor.execute(sql)
            self.db.commit()
            connfd.send(b"OK")
        except Exception:
            self.db.rollback()
            connfd.send(b"FAIL")


#郑琪胜

    # 申请报销
    def do_reim(self,connfd,user,cursor):
        '''报销程序,将员工报销信息插入到数据库员工报销表,并返回提交结果'''
        user_id = user
        connfd.send(b'REIMOK')
        response = connfd.recv(4096).decode()
        if response == 'OUT':
            return
        reimmoney,reimdesc =  response.split('##')
        sql = "insert into user_reim(user_id, money, reim_desc)values ('%s', '%s', '%s');" % (user_id, reimmoney, reimdesc)
        try:
            cursor.execute(sql)
            self.db.commit()
            connfd.send(b"OK")
        except Exception:
            self.db.rollback()
            connfd.send(b"FAIL")

    # 审核报销
    def do_auditing(self,connfd,user,cursor):
        '''领导审核报销程序'''
        user_id = user
        connfd.send(b'OK')
        while True:
            response = connfd.recv(128).decode()
            if response == 'EXIT':
                return
            data, desc= response.split('##')
            # 审核所有待审核报销
            if data == '1':
                # 根据领导id得到部门编号,再根据部门编号得到该部门所有员工id,再查询到这些员工id对应的报销申请
                sql = "select * from user_reim where is_approve = '未审核' and user_id in (select user_id from user_info where pro_no = (select pro_no from user_info where user_id = '%s'));" % user_id
                reimnum = cursor.execute(sql) # 获取执行条数
                
                reimdata = cursor.fetchall() # 获取所有数据 大元组里套小元组
                content = ''
                for x in reimdata:
                    content += x.__str__() + '##'
                if reimnum == 0:
                    connfd.send(b'END')
                    return
                else:
                    connfd.send(content.encode())
                    return

    def do_auditing_handle(self,connfd,cursor):
        connfd.send(b'OK')
        response = connfd.recv(128).decode().split('##')
        reim_id = response[0]
        option = response[1]
        if option == '1':
            sql = 'update user_reim set is_approve = "同意" where reim_id = "%s" ;' % reim_id
        elif option == '2':
            sql = 'update user_reim set is_approve = "驳回" where reim_id = "%s" ;' % reim_id
        try:
            cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            connfd.send(b"ERR")
        if option == '1':
            connfd.send(b"OK1")
        else:
            connfd.send(b"OK2")


    # 员工报销申请全部发送完毕后

            # 根据id得到特定用户待审核报销
            # elif data == '2':
            #     # reimdesc:审核 , reim_id : 接收到的员工id
            #     reimdesc,reim_id = desc.split('$$')
            #     # 查询属于登陆领导的所有下属员工
            #     sql_YN = "select user_id from user_info where pro_no = (select pro_no from user_info where user_id = '%s');" % user_id
            #     cursor.execute(sql_YN)
            #     reim_pro_user = cursor.fetchall()
            #     # 如果该员工不属于登陆领导
            #     flag = False
            #     for x in reim_pro_user: # x为小元组,即该部门所有员工id
            #         for y in x:  # 遍历出每个员工id
            #             if reim_id == y :
            #                 flag = True 
            #     if flag == False:
            #         connfd.send(b'NOPOW')
            #         continue
            #     sql = 'select * from user_reim where is_approve = "未审核" and user_id = "%s";' % reim_id

            # reimnum = cursor.execute(sql) # 获取执行条数
            # reimdata = cursor.fetchall() # 获取所有数据 大元组里套小元组
            # if reimnum == '0':
            #     connfd.send(b'END')
            #     continue
            # else:
            #     for reim_data in reimdata:
            #         reim_str = reim_data[1]+'##'+reim_data[2]+'##'+reim_data[3]
            #         connfd.send(reim_str.encode())
            #         result = connfd.recv(4096).decode()
            #         if result == '1':
            #             sql = 'update user_reim set is_approve = "同意" where reim_id = "%s" ;' % reim_data[0]
            #         elif result == '2':
            #             sql = 'update user_reim set is_approve = "驳回" where reim_id = "%s" ;' % reim_data[0]
            #         try:
            #             cursor.execute(sql)
            #             self.db.commit()
            #         except Exception as e:
            #             connfd.send(b"ERR")
            #         else:
            #             connfd.send(b"OK")
            #             gonext = connfd.recv(4096).decode()
            #             # 接收到信息后,继续发送下一个数据
            #             if gonext == 'GO':
            #                 continue

            #     # 员工报销申请全部发送完毕后
            #     connfd.send(b"END")
            #     continue


    # 查询报销申请
    def read_reim(self,connfd,user,cursor):
        '''查看报销申请程序'''
        user_id = user
        # 如果是领导查询,返回该部门所有报销申请
        if user_id[0] == 'l':
            # 根据领导id得到部门编号,再根据部门编号得到该部门所有员工id,再查询到这些员工id对应的报销申请
            sql = "select * from user_reim where user_id in (select user_id from user_info where pro_no = (select pro_no from user_info where user_id = '%s'));" % user_id
        # 如果是员工查询,返回该员工所有的报销申请
        elif user_id[0] == 'n':
            sql = 'select * from user_reim where user_id = "%s";' % user_id
        reimnum = cursor.execute(sql) # 获取执行条数
        reimdata = cursor.fetchall() # 获取所有数据
        if reimnum == '0':
                connfd.send(b'ENDZERO')
                return
        else:
            for reim_data in reimdata:
                # read_str = reim_data[0]+'##'+reim_data[1]+'##'+reim_data[2]+'##'+reim_data[3]+'##'+reim_data[4]
                read_str = "%s##%s##%s##%s##%s" % (reim_data[0],reim_data[1],reim_data[2],reim_data[3],reim_data[4])
                connfd.send(read_str.encode())
                result = connfd.recv(4096).decode()
                # 发送信息后,等待客户端回应,继续发送下一个数据
                if result == 'GO':
                    continue
            # 所有报销申请全部发送完毕后
            connfd.send(b"ENDALL")
            return

#王鹏
# 查询公告函数
    def select_notice(self,connfd,user,cursor):
        # 调用此函数,发送确认连接
        connfd.send(b'ok')
        # 1.查询操作
        option = connfd.recv(128).decode()
        if option == 'EXIT':
            return

        elif option == '2':


            connfd.send(b'ok')

            noticedate = connfd.recv(128).decode()
            sql = "select * from work_sign where substr(issue_time,1,10)= '%s'" % noticedate
            
        elif option == '1':
            sql = "select * from work_sign"
            
        try:
            
            cursor.execute(sql)  # 执行sql语句
            str1 = ''
            results = cursor.fetchall()  # 获取查询的所有记录
            for res in results:
                str1 += res.__str__() + "##"
            if results == ():
                connfd.send(b'null')
            else:
                connfd.send(str1.encode())

        except Exception as e:
            connfd.send(b'null')
#--------------#超级用户创建新用户--------------------
    def supercreate(self,connfd,cursor):
        connfd.send(b"OK")
        while True:
            response = connfd.recv(128).decode()
            choose = response.split("###")[0]

            #创建用户
            if choose == "#C":
                sql = "select user_id from user_passwd where user_id = '%s'" % response.split("###")[1]
                try:
                    cursor.execute(sql)
                except Exception:
                    connfd.send(b"ERR")
                else:
                    r = cursor.fetchall()
                    if len(r) == 0:
                        sql = 'insert into user_passwd values("%s","%s");' % \
                            (response.split("###")[1],response.split("###")[2])
                        try:
                            cursor.execute(sql)
                            sql1 = 'insert into user_info values("%s","%s","%s","%s","%s");' \
                                % (response.split("###")[1],response.split("###")[3],response.split("###")[4],\
                                response.split("###")[5],response.split("###")[6])
                            try:

                                cursor.execute(sql1)
                                
                                self.db.commit()
                                connfd.send(b"OK")
                            except Exception:
                                self.db.rollback()
                                connfd.send(b"FAIL")
                        except Exception:
                            self.db.rollback()
                            connfd.send(b"FAIL")
                    else:
                        connfd.send(b"RE")

            #删除用户
            elif choose == "#D":
                sql = "select user_id from user_passwd where user_id = '%s'" % response.split("###")[1]
                try:
                    cursor.execute(sql)
                except Exception:
                    connfd.send(b"ERR")
                r = cursor.fetchall()
                if len(r) != 0:
                    sql = 'delete from user_passwd where user_id = "%s";delete from user_info where user_id = "%s";delete from user_reim where user_id = "%s";delete from userwork where user_id = "%s"' % (response.split("###")[1],response.split("###")[1],response.split("###")[1],response.split("###")[1])
                    try:
                        cursor.execute(sql)
                        self.db.commit()
                        connfd.send(b"OK")
                    except Exception:
                        self.db.rollback()
                        connfd.send(b"FAIL")
                else:
                    connfd.send(b"RE")
            
            #创建公告
            elif choose == "#S":
                connfd.send(b"OK")
                dataname = connfd.recv(128).decode()
                connfd.send(b"OK")
                data = ''
                while True:
                    content = connfd.recv(4096).decode()
                    time.sleep(0.1)
                    if content == "##":
                        break
                    data += content
                sql = "insert into work_sign(signname,content,issue_time) values('%s','%s',now());" % (dataname,data)
                try:
                    cursor.execute(sql)
                    self.db.commit()
                    connfd.send(b"SURE")
                except Exception:
                    self.db.rollback()
                    connfd.send(b"FAIL")
            #删除公告
            elif choose == "#I":
                drop_id = response.split('###')[1]
                sql = "delete from work_sign where id = '%s';" % drop_id
                try:
                    cursor.execute(sql)
                    self.db.commit()
                    connfd.send(b"SURE")
                except Exception:
                    self.db.rollback()
                    connfd.send(b"FAIL")

        
#--------------------------------------------------


        
        

        


    


    

if __name__ == '__main__':
    userver = Userver(address_user)
    userver.start_server() #启动服务



