# -*- coding:utf-8 -*-
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


class MysqlSearch(object):
    #__DBFILE = ""
    __HOST = ""
    __USER = ""
    __PASSWORD = ""
    __DBNAME = ""
    __CONNECTION = None
    __CURSOR = None
    __MODE = "S"
    CONNECTED = False
    sqlserver = True
    __opentime = 0  # Open时的系统时间,用于计算连接创建时长,时间过长则关掉重新创建.
    MaxConnectTime = 60 * 5  # 20分钟重新连接一次
    DEBUGING = False

    # server = "10.10.70.89"    # 连接服务器地址
    # user = "sa"     # 连接帐号
    # password = "123456" # 连接密码
    # conn = pymssql.connect(server, user, password, "IPEasy")  #获取连接
    # cursor = conn.cursor(as_dict=True)  # 获取光标
    # cursor.execute('SELECT case_volume,app_date,charge_date,examime_date FROM p_case_info ')


# 数据库
# mysql = MysqlSearch("10.10.70.88","atw","root","atw", False)
