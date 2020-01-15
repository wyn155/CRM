# -*- coding:utf-8 -*-
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import traceback, sys, json
import time,re
import datetime

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
    MaxConnectTime = 60 * 15  # 15分钟重新连接一次
    DEBUGING = False

    # server = "10.10.70.89"    # 连接服务器地址
    # user = "sa"     # 连接帐号
    # password = "123456" # 连接密码
    # conn = pymssql.connect(server, user, password, "IPEasy")  #获取连接
    # cursor = conn.cursor(as_dict=True)  # 获取光标
    # cursor.execute('SELECT case_volume,app_date,charge_date,examime_date FROM p_case_info ')

    def __init__(self, host, user, pwd, db, sqlserver=True):  # 数据库文件路径
        self.__HOST = host
        self.__USER = user
        self.__PASSWORD = pwd
        self.__DBNAME = db
        self.sqlserver = sqlserver
        # self.__HOST = "localhost"
        # self.__USER = "root"
        # self.__PASSWORD = "12345"
        # self.__DBNAME = "test"

    def __Connect(self):  # 连接动作
        try:
            if self.sqlserver:
                self.__CONNECTION = pymssql.connect(self.__HOST, self.__USER, self.__PASSWORD, self.__DBNAME)
            else:
                self.__CONNECTION = pymysql.connect(self.__HOST, self.__USER, self.__PASSWORD, self.__DBNAME)
            self.__CURSOR = self.__CONNECTION.cursor()
            # self.__CURSOR = self.__CONNECTION.cursor(as_dict=True)
            self.CONNECTED = True
            self.__MODE = "M"
        except Exception as e:
            print(sys._getframe().f_code.co_name, e)
            if self.DEBUGING:
                print(traceback.print_exc())

    def Commit(self):  # 提交
        self.__CONNECTION.commit()

    def __DisConnect(self):
        self.__CURSOR.close()
        self.__CONNECTION.close()
        self.CONNECTED = False
        self.__MODE = "S"

    def __CheckConnectTime(self):
        if self.__opentime == 0:  # S模式(单执行模式)不计算连接时间,只有在M模式(多执行模式)下计算连接时间.
            return
        nowtime = time.time()
        connecttime = nowtime - self.__opentime
        if connecttime > self.MaxConnectTime:
            self.__ReConnect()

    def __ReConnect(self):
        if self.__MODE == "M":
            try:
                self.Close()
            finally:
                self.Open()

    def Open(self):
        self.__Connect()
        if self.CONNECTED:
            self.__MODE = "M"

    def Close(self):
        self.__CONNECTION.commit()
        self.__DisConnect()
        self.__CONNECTIONSTATE = False
        if not self.CONNECTED:
            self.__MODE = "S"

    def Query(self, sql, top=0):  # 如果top=1，则只返回第一条数据
        try:
            if self.__MODE == "S":
                self.__Connect()
            SQLString = sql
            # print(sql)
            self.__CURSOR.execute(SQLString)
            if top == 0:
                data = self.__CURSOR.fetchall()
                if len(data) == 0:
                    return data
                if len(data[0]) == 1:
                    rtnv = []
                    for d in data:
                        rtnv.append(d[0])
                    return rtnv
                return data
            else:
                data = self.__CURSOR.fetchone()
                if data == None or len(data) == 0:
                    return data
                if len(data) == 1:  # 只有一列的情况
                    rtnv = data[0]
                    return rtnv
                rtnv = []
                for d in data:
                    rtnv.append(d)
                return rtnv
        except Exception as e:
            print(sys._getframe().f_code.co_name, e)
            if self.DEBUGING:
                print(traceback.print_exc())
        finally:
            if self.CONNECTED or self.__MODE == "M":
                self.__DisConnect()

    def query(self, tbl, key_list, pk_dict={}, pkstr="", num=None):
        if type(tbl) != type("") or type(key_list) != type([]) or type(pk_dict) != type({}) or type(pkstr) != type(""):
            print("参数类型不正确")
        if pk_dict and pkstr:
            print("判断条件只能输入一种，字典或“where ...”字符串")
        try:
            if self.__MODE == "S" or not self.CONNECTED:
                self.__Connect()
            s1 = "select "
            s = []
            s2 = " from {} ".format(tbl)
            t = []
            l = " limit {}".format(num) if num else ""
            s = ",".join(key_list)
            if pk_dict:
                for pk in pk_dict:
                    t.append(pk + "='" + str(pk_dict[pk]) + "'")
                t = " and ".join(t)
                t = "where " + t if pk_dict else ""
                SQLString = s1 + s + s2 + t + l
            if pkstr:
                SQLString = s1 + s + s2 + pkstr + l
            print(SQLString)
            self.__CURSOR.execute(SQLString)
            data = self.__CURSOR.fetchall()
            if len(data) > 0:
                rtnv = []
                for d in data:
                    res = {}
                    for i in range(len(key_list)):
                        res[key_list[i]] = str(d[i])
                    rtnv.append(res)
                return rtnv
            else:
                return data
        #
        except Exception as e:
            print(sys._getframe().f_code.co_name, e)
            if self.DEBUGING:
                print(traceback.print_exc())
        finally:
            if self.CONNECTED or self.__MODE == "M":
                self.__DisConnect()


    def Insert_dict(self, tbl, data_dict, commit=True):
        if type(tbl) != type("") or type(data_dict) != type({}):  print("参数类型不正确")
        try:
            if self.__MODE == "S":
                self.__Connect()
            s1 = "insert into " + tbl + "("
            v1 = ""  # "a,b,c,d"
            s2 = ") values("
            v2 = ""  # "%s,%s,%s,%s"
            s3 = ")"
            #            param=[]
            for i in data_dict:
                v1 += "," + i
                tmp = data_dict[i] if type(data_dict[i]) == type("") else str(data_dict[i])
                v2 += ",'" + tmp + "'"
            # param.append(data_dict[i])
            v1 = v1[1:len(v1)]
            v2 = v2[1:len(v2)]
            SQLString = s1 + v1 + s2 + v2 + s3
            print(SQLString)
            self.__CURSOR.execute(SQLString)
            if commit:
                self.__CONNECTION.commit()
            # n_count = self.__CURSOR.rowcount
            # return n_count
            return "success"
        except Exception as e:
            print(sys._getframe().f_code.co_name, e)
            if self.DEBUGING:
                print(traceback.print_exc())
            return "fail"
        finally:
            if self.CONNECTED or self.__MODE == "M":
                self.Commit()
                self.__DisConnect()

    def Insert_list(self, tbl, data_list, commit=True):
        if type(tbl) != type("") or type(data_list) != type([]):  print("参数类型不正确")
        try:
            if self.__MODE == "S":
                self.__Connect()
            s1 = "insert into " + tbl + " values("
            v2 = ""  # "%s,%s,%s,%s"
            s3 = ")"
            for i in data_list:
                tmp = i if type(i) == type("") else str(i)
                v2 += ",'" + tmp + "'"
            v2 = v2[1:len(v2)]
            SQLString = s1 + v2 + s3
            self.__CURSOR.execute(SQLString)
            if commit:
                self.__CONNECTION.commit()
            # n_count = self.__CURSOR.rowcount
            return "success"
        except Exception as e:
            print(sys._getframe().f_code.co_name, e)
            if self.DEBUGING:
                print(traceback.print_exc())
            return "fail"
        finally:
            if self.CONNECTED or self.__MODE == "M":
                self.Commit()
                self.__DisConnect()


    def Update_dict(self, tbl, data_dict, pk_dict, commit=True):
        if type(tbl) != type("") or type(data_dict) != type({}) or type(pk_dict) != type({}):  print("参数类型不正确")
        try:
            if self.__MODE == "S":
                self.__Connect()
            s1 = "update " + tbl + " set "
            s = []
            s3 = " where "
            t = []
            for data in data_dict:
                s.append(data + "='" + str(data_dict[data]) + "'")
            for pk in pk_dict:
                t.append(pk + "='" + str(pk_dict[pk]) + "'")
            s = ",".join(s)
            t = " and ".join(t)
            SQLString = s1 + s + s3 + t
            print(SQLString)
            r = self.__CURSOR.execute(SQLString)
            if commit:
                self.Commit()
            return "success"
        except Exception as e:
            print(sys._getframe().f_code.co_name, e)
            if self.DEBUGING:
                print(traceback.print_exc())
            return "fail"
        finally:
            if self.CONNECTED or self.__MODE == "M":
                self.Commit()
                self.__DisConnect()

    def Exec(self, sql, commit=True):
        try:
            if self.__MODE == "S":
                self.__Connect()
            SQLString = sql
            print(sql)
            if re.search(";",sql):
                sqllist = sql.split(";")
                for i in sqllist:
                    self.__CURSOR.execute(i)
            else:
                self.__CURSOR.execute(SQLString)
            if commit:
                self.__CONNECTION.commit()
            # n_count = self.__CURSOR.rowcount
            # return n_count
            return "success"
        except Exception as e:
            print(sys._getframe().f_code.co_name, e)
            if self.DEBUGING:
                print(traceback.print_exc())
            return "fail"
        finally:
            if self.CONNECTED or self.__MODE == "M":
                self.__DisConnect()



# mysql 数据库
mysql = MysqlSearch("10.10.70.88","atw","root","atw", False)
# wdsql = MysqlSearch("10.10.70.89","sa","123456","IPEasy")
