#encoding=utf-8
# st = u'2015年07月15日'
st = u'今天15:30'
import re
from pprint import pprint
from datetime import date,time,datetime
def extracttime(s):
    s = s.strip()
    print(s)
    if s:
        if s.find(u'今天') != -1:
            Date = datetime.today().date()
            res = re.search(r'今天(?P<hour>\d+):(?P<minute>\d+)',s.encode('utf-8'))
            Time = time(int( res.group('hour') ),int( res.group('minute') ) )
            return Date,Time
        res = re.search(r'((?P<year>\d+)年)?(?P<month>\d+)月(?P<day>\d+)日(.*(?P<hour>\d+):(?P<minute>\d+).*)?', s.encode('utf8'))
        if res:
            print(res.groups())
            year = res.group('year')
            month = res.group('month')
            day = res.group('day')
            hour = res.group('hour')
            minute = res.group('minute')
            x = date(int(year),int(month),int(day))
            y = time(hour=int(hour),minute = int(minute))
            print(x,y)
            # time = datetime.datetime.strftime('st')
            return {"year": year, "month": month, "day": day, "hour": hour, "minute": minute}

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
time.sleep(5)
from mysql.connector import connection
cnx = connection.MySQLConnection(user='root',password='',database='sinaData')
cursor = cnx.cursor()
print("yes")
