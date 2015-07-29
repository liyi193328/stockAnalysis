# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from mysql.connector import connection
from datetime import datetime,date,time

class SinacrawlerPipeline(object):

    articleTablePre = 'sinaArticles'

    def __init__(self):

        self.cnx = connection.MySQLConnection(user='root',password='',database='sinaData')
        self.cursor = self.cnx.cursor()
        print('connection to sinaData suc')

    def connectDB(self):
        self.cnx = connection.MySQLConnection(user='root',password='',database='sinaData')
        self.cursor = self.cnx.cursor()
        print("connect mysql sinaData suc!")

    def insertDict(self,item):
        self.connectDB()
        tablename = self.articleTablePre + item['stockTable']
        newDict = dict()
        for key,values in item.items():
            if key != 'stockTable':
                text = values
                if type(values) == list:
                    tem = None
                    for ev  in values:
                        tem += ev
                    text = tem
                newDict[key] = text
        newDict['crawlDate'] = date.today()

        placeholders = ', '.join(['%s'] * len(newDict))
        columns = ', '.join(newDict.keys())
        sql = "insert ignore into %s ( %s ) VALUES ( %s )" % (tablename, columns, placeholders)
        self.cursor.execute(sql, newDict.values())
        self.cnx.commit()
        print('insert suc!')

    def process_item(self, item, spider):

        self.insertDict(item)

        return item

    def close_spider(self,spider):
        self.cnx.close()
        self.cursor.close()