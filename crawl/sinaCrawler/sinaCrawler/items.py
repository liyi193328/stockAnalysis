# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class sinaArticleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ####文章###
    title = scrapy.Field()  #标题
    content = scrapy.Field()  #内容
    date = scrapy.Field()   #日期,year,month,day
    time = scrapy.Field()   #hour,minute,second
    contentFrom = scrapy.Field()   #发表机构
    url = scrapy.Field()  #文章的url
    stockTable = scrapy.Field()  #文章对于的股票表名(数据库中)
    crawlDate = scrapy.Field()
