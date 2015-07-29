import re
from datetime import date,time,datetime

def extracttime(s):
    s = s.strip()
    if s:
        if s.find(u'今天') != -1:
            Date = datetime.today().date()
            res = re.search(r'今天(?P<hour>\d+):(?P<minute>\d+)',s.encode('utf-8'))
            Time = time(int( res.group('hour') ),int( res.group('minute') ) )
            return Date,Time

        if s.find(u'分钟前') != -1:
            res = re.search(r'(\d+).*分钟.*',s.encode('utf-8'))
            if res:
                DateTime = datetime.today() - timedelta(minutes=int( res.group(1) ) )
                return DateTime.date(),DateTime.time()

        if s.find(u'小时前') != -1:
            res = re.search(r'(\d+).*小时.*',s.encode('utf-8'))
            if res:
                DateTime = datetime.today() - timedelta(hours=int( res.group(1) ) )
                return DateTime.date(),DateTime.time()
        if s.find(u'天前') != -1:
            res = re.search(r'(\d+).*天前.*',s.encode('utf-8'))
            if res:
                DateTime = datetime.today() - timedelta(days=int( res.group(1) ) )
                return DateTime.date(),DateTime.time()
        if s.find(':') == -1:
            res = re.search(r'((?P<year>\d+)年)?(?P<month>\d+)月(?P<day>\d+)日',s.encode('utf-8'))
            if res:
                year = res.group('year')
                month = res.group('month')
                day = res.group('day')
                if year == None:
                    year = 2015
                if month == None:
                    month = datetime.today().date().month
                if day == None:
                    day = datetime.today().date().month
                return date(int(year),int(month),int(day)),time(0,0,0)

        res = re.search(r'((?P<year>\d+)年)?(?P<month>\d+)月(?P<day>\d+)日.*(?P<hour>\d+):(?P<minute>\d+).*', s.encode('utf8'))
        if res:
            year = res.group('year')
            month = res.group('month')
            day = res.group('day')
            hour = res.group('hour')
            minute = res.group('minute')
            if year == None:
                year = 2015
            if hour == None:
                hour = 0
            if minute == None:
                minute = 0
            Date = date(int(year),int(month),int(day))
            Time = time(hour=int(hour),minute = int(minute))
            return Date,Time
    return date(1,1,1),time(0,0,0)  
