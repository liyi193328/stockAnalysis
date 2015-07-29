# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class sinabbsPost(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ##帖子#####
    title = scrapy.Field()   #帖子标题，在x页面
    url = scrapy.Field()   #帖子的url
    clickNum = scrapy.Field()  #点击数目（阅读数）
    replyNum = scrapy.Field()  #回复数
    author = scrapy.Field()  #发帖人
    date = scrapy.Field()  #帖子日期
    time = scrapy.Field()  #帖子时间
    content = scrapy.Field() #帖子内容
    url = scrapy.Field()  #帖子url
    stockTable = scrapy.Field() #帖子对于的股票表名(数据库中)
    crawlDate = scrapy.Field()

class sinabbsReply(scrapy.Item):
    url = scrapy.Field()  #帖子的url
    commentUser = scrapy.Field()  #回复人
    commentDate = scrapy.Field() #回复日期（没有时间)
    commentContent = scrapy.Field() # 回复内容
    stockTable = scrapy.Field()  #回复对于的股票表名(数据库中)
    crawlDate = scrapy.Field()