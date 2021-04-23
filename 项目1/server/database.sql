create table user_info(
    user_id varchar(20) primary key comment '员工编号',
    user_name varchar(50) comment '员工姓名',
    user_phone varchar(20) comment '员工电话',
    pro_no varchar(20) comment '部门编号',
    balance_flag int comment '员工工资标准')charset=utf8;

mysql> select * from user_info;
<!--python3 super_user.py 以后跟着输入就行-->
+---------+-----------+------------+--------+--------------+-------------+---------------+
| user_id | user_name | user_phone | pro_no | balance_flag | user_leadno | user_leadname |
+---------+-----------+------------+--------+--------------+-------------+---------------+
| l1002   | 申童      | 1325665343 | 002    |         5000 | 002         | 002           |
+---------+-----------+------------+--------+--------------+-------------+---------------+



create table user_passwd(
    user_id varchar(20) primary key comment '员工编号',
    passwd varchar(20) comment '密码'
)charset=utf8;
<!--python3 super_user.py 以后跟着输入就行-->

mysql> select * from user_passwd;
+---------+----------+
| user_id | passwd   |
+---------+----------+
| l1002   | shentong |
+---------+----------+


create table work_sign(
id int auto_increment primary key,
signname varchar(200),
content varchar(1000),
issue_time datetime)charset=utf8;
<!--python3 super_user.py 以后跟着输入就行-->
mysql> select * from work_sign;
+----+-----------------+--------------------------+---------------------+
| id | signname        | content                  | issue_time          |
+----+-----------------+--------------------------+---------------------+
|  2 | 第一个公告      | 第一个公告的内容         | 2019-03-11 23:54:19 |
+----+-----------------+--------------------------+---------------------+


CREATE TABLE userwork (
  user_id varchar(20),
  iswork varchar(10),
  worktime datetime,
  workdesc varchar(200),
  isagree varchar(10)
)charset=utf8;
--客户端打卡选项自己输入就行
mysql> select * from userwork;
+---------+--------+---------------------+--------------+---------+
| user_id | iswork | worktime            | workdesc     | isagree |
+---------+--------+---------------------+--------------+---------+
| l1002   | 1      | 2019-03-11 23:41:42 | SUCCESS      | 1       |
| l1002   | 2      | 2019-03-11 23:42:26 | 请年假       | 2       |
| l1002   | 3      | 2019-03-11 23:42:46 | 请其他假     | 2       |
| l1002   | 1      | 2019-03-11 23:46:15 | SUCCESS      | 1       |
+---------+--------+---------------------+--------------+---------+



帐号密码表 user_passwd
user_id 帐号(员工编号)
passwd 密码

员工信息表 user_info
user_id 员工编号
user_name 员工姓名
user_phone 员工电话
pro_no 部门编号
balance_flag 员工工资标准
user_leadno  直属领导/所属员工编号
user_leadname  领导/所属员工姓名

员工出勤表 userwork
user_id 员工编号
iswork 打卡状态
worktime 打卡时间
workdesc 请假注释
isagree 是否审批

员工报销审批表 user_reim
user_id 员工编号
money 报销金额
reim_desc 报销注释
is_approve 是否审批

公告表 work_sign(super用户设置)
id 编号
signname 公告名
content 内容
issue_time 发布时间


--直接use userattr;后复制粘帖就行
DELIMITER $$
CREATE FUNCTION workdaynum(datefrom date,dateto date) 
RETURNS int(20) NO SQL
BEGIN
    declare days int default 1;
    if (datefrom > dateto  or year(datefrom) != year(dateto)) then  
        return -1;
        end if;
	set days = 
        case when week(dateto)-week(datefrom) = 0 then
            dayofweek(dateto) - dayofweek(datefrom) + 1
        - case when (dayofweek(datefrom) > 1 and dayofweek(dateto) < 7) then 0
            when (dayofweek(datefrom) = 1 and dayofweek(dateto) =7) then 2
            else 1
            end
        else (week(dateto)-week(datefrom)-1) * 5
            + case when dayofweek(datefrom) = 1 then 5
            when dayofweek(datefrom) = 7 then 0
            else 7 - dayofweek(datefrom)
            end
            + case
            when dayofweek(dateto) = 1 then 0
            when dayofweek(dateto) = 7 then 5
            else dayofweek(dateto) - 1
            end
        end;
    return days;
end$$
DELIMITER ;

create table user_reim (reim_id int(11) primary key auto_increment,user_id varchar(100),money varchar(100),reim_desc varchar(1000),is_approve varchar(1000) default '未审核')charset=utf8;


