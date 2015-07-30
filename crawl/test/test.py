#encoding=utf-8
# st = u'2015年07月15日'
st = u'2月29日'
import re
from pprint import pprint
from datetime import date,time,datetime
# Date,Time = extracttime(st)
# print(Date)
# print(Time)
# flist = open('nameList(sina).txt','r+')
# for ev in flist.readlines():
#     ev = ev.decode('utf-8')
#     st = ev.split(u"    ")
#     print(st[0])
# x = u'李奕'
# print(x.find(u'xx'))
import time
from mysql.connector import connection
cnx = connection.MySQLConnection(user='root',password='',database='sinaData')
cursor = cnx.cursor()
print("yes")
