# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from mysql.connector import connection
from sinabbsCrawler.items import sinabbsPost,sinabbsReply
from datetime import datetime,date,time
from sinabbsCrawler.items import sinabbsPostNum

class SinabbscrawlerPipeline(object):

    postTablePre = 'sinabbsPosts'
    replyTablePre = 'sinabbsReplies'
    postNumTablePre = 'sinabbsPostsNum'

    def __init__(self):
        self.cnx = connection.MySQLConnection(user='root',password='',database='sinaData')
        self.cursor = self.cnx.cursor()
        print("init: connect mysql sinaData suc!")

    def connectDB(self):
        self.cnx = connection.MySQLConnection(user='root',password='',database='sinaData')
        self.cursor = self.cnx.cursor()
        print("connect mysql sinaData suc!")

    def insertDict(self,item):
        self.connectDB()

        # print(item.keys(),item['stockTable'].encode('utf-8'))
        # input("keys:")
        tablename = item['stockTable']
        if isinstance(item,sinabbsPost):
            tablename = self.postTablePre + tablename
        elif isinstance(item,sinabbsPostNum):
            tablename = self.postNumTablePre + tablename
        else:
            tablename = self.replyTablePre + tablename
        # item.pop('stockTable')  ###keng
        newDict = dict()
        for key,values in item.items():
            if key != 'stockTable':
                newDict[key] = values
        newDict['crawlDate'] = date.today()
        
        placeholders = ', '.join(['%s'] * len(newDict))
        columns = ', '.join(newDict.keys())
        sql = "insert ignore into %s ( %s ) VALUES ( %s )" % (tablename, columns, placeholders)
        self.cursor.execute(sql, newDict.values())
        self.cnx.commit()
        print('insert suc!')
        # input("insert suc:")
    def constructPostNumFromPost(self,item):
        keys = ['stockTable','url','clickNum','replyNum','date','time']
        postNum = sinabbsPostNum()
        for key in keys:
            postNum[key] = item[key]
        return postNum

    def process_item(self, item, spider):

        if isinstance(item,sinabbsPost):
            self.insertDict(item)
            print "sinabbsPost"
            postNum = self.constructPostNumFromPost(item)
            self.insertDict(postNum)
            print("sinabbsPostNum")

        else:
            self.insertDict(item)
            print "reply"

        return item

    def debugItem(self,item):
        if isinstance(item,sinabbsPost):
            print('post of %s' %item['url'])
            # self.fp.write('post of %s' %item['url']+'\n')
            for key,value in item.items():
                print key
                # self.fp.write(key+'\n')
                if key != 'date' and key != 'time':
                    print value.encode('utf-8')
                    # self.fp.write(value.encode('utf-8')+'\n')
                else:
                    print value
                    # self.fp.write(str(value).encode('utf-8')+'\n')

        elif isinstance(item,sinabbsReply):
            print('Reply for %s' %item['url'])
            # input("reply:")
            # self.fp.write('Reply for %s' %item['url']+'\n')
            for key,value in item.items():
                print key
                # self.fp.write(key+'\n')
                if key != 'commentDate':
                    print value.encode('utf-8')
                    # self.fp.write(value.encode('utf-8')+'\n')
                else:
                    print value
                    # self.fp.write(value.encode('utf-8')+'\n')
                    
    def close_spider(self,spider):
        self.cnx.close()
        self.cursor.close()