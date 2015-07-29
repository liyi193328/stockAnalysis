from mysql.connector import connection
from datetime import datetime,time,date,timedelta

class DB:
    def __init__(self):
        self.cnx,self.cursor = self.connectMysql('root','','sinaData')
        self.f = open('namelist.txt','r+')

    def connectMysql(self,User='root',Password='',Database='sinaData'): 
        cnx = connection.MySQLConnection(user=User,password=Password,database=Database)
        cursor = cnx.cursor()
        return cnx,cursor

    def testCreate(self):
        st = (
        " CREATE TABLE if not exists `dept_manager` ("
        " `dept_no` char(4) NOT NULL,"
        " `emp_no` int(11) NOT NULL,"
        " `from_date` date NOT NULL,"
        " `to_date` date NOT NULL,"
        " PRIMARY KEY (`emp_no`,`dept_no`),"
        "unique key `url_unique` (`emp_no`)"
        ") ENGINE=InnoDB")
        self.cursor.execute(st)
        self.cnx.commit()
    def testInsert(self):

        tomorrow = datetime.now().date() + timedelta(days=1)

        add_salary = ("INSERT ignore INTO dept_manager "
        "(emp_no, dept_no, from_date, to_date) "
        "VALUES (%(emp_no)s, %(dept_no)s, %(from_date)s, %(to_date)s)")
        data_employee = ('Geert', 'Vanderkelen', tomorrow, 'M', date(1977, 6, 14))

        # Insert salary information
        data_salary = {
        'emp_no': 5,
        'dept_no': '20',
        'from_date': tomorrow,
        'to_date': date(9999, 1, 1),
        }
        self.cursor.execute(add_salary, data_salary)
        self.cnx.commit()

    def createTables(self):
        alllines = self.f.readlines()
        cnt = 0
        for i in range(1,len(alllines)):
            cnt += 1
            line = alllines[i]
            stockCode =  line.split(' ')[-1]
            st = str(stockCode).strip()
            article = 'sinaArticles'+st
            bbsPost = 'sinabbsPosts'+st
            bbsReply = 'sinabbsReplies'+st

            self.createArticleTable(article)
            self.createbbsPostTable(bbsPost)
            self.createbbsReplyTable(bbsReply)
            self.cnx.commit()
        print(cnt)

    def createDB(self,dbname):
        # st = " DEFAULT CHARSET utf8 COLLATE utf8_general_ci"
        # sen = (
        #     "CREATE DATABASE %(dbname)s" 
        #     )
        # par = {
        # "dbname":dbname,
        # }

        # self.cursor.execute(sen,par)

        sen = "CREATE DATABASE IF NOT EXISTS %s DEFAULT CHARSET utf8 COLLATE utf8_general_ci"%dbname
        self.cursor.execute(sen)
        self.cnx.commit()

    def deleteDatabase(self,dbname):
        sen = "drop database if exists %s" %dbname
        self.cursor.execute(sen)
        self.cnx.commit()
        print("del database %s"%dbname)

    def delTable(self,tablename):
        sen = "truncate table %s" %tablename
        self.cursor.execute(sen)
        self.cnx.commit()
        print("del table %s"%tablename)

    def createArticleTable(self,article):
        sen = (
                "create table if not exists %s ("
                " `id` bigint(11) not null auto_increment,"
                " `title` varchar(255) null,"
                " `content` mediumtext null,"
                " `date` date null,"
                " `time` time null,"
                " `url` varchar(255) null,"
                " `contentFrom` varchar(255) null,"
                "  `crawlDate` date not null," 
                " unique key `url_unique` (`url`),"
                "primary key(`id`)"
                ")DEFAULT CHARACTER SET = utf8" 
            )%(article)
        print(sen)
        self.cursor.execute(sen)
        self.cnx.commit()

        # print(sen)
    def createbbsPostTable(self,bbsPost):
        sen = (
                "create table if not exists %s ("
                " `id` bigint(11) not null auto_increment,"
                " `title` varchar(255) null, "
                " `url` varchar(255) not null, "
                " `clickNum` int null,"
                " `replyNum` int null,"
                " `author` varchar(255) null, "
                " `date` date null,"
                " `time` time null,"
                " `content` mediumtext null, "
                "  `crawlDate` date not null," 
                " unique key `url_unique` (`url`),"
                " primary key(`id`)"
                ")DEFAULT CHARACTER SET = utf8"
            )%(bbsPost)
        print(sen)
        self.cursor.execute(sen)

    def createbbsReplyTable(self,bbsReply):
        sen = (
                "create table if not exists %s ("
                " `id` bigint(11) not null auto_increment,"
                " `commentUser` varchar(255) null, "
                " `commentDate` date null,"
                " `commentContent` text null, "
                " `url` varchar(255) null, "
                "  `crawlDate` date not null," 
                " primary key(`id`),"
                " unique key `reply_unique` (`commentUser`,`commentDate`,`commentContent`(11))"
                ")DEFAULT CHARACTER SET = utf8"
            )%(bbsReply)
        print(sen)
        self.cursor.execute(sen)

db = DB()
# db.testCreate()
# db.createArticleTable("liyi")
db.createTables()
# db.testCreate()
# db.testInsert()
# db.createDB("xx")

