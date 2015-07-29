# encoding=utf-8

import scrapy,os,re
from pprint import pprint
from marionette import Marionette
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import time,date,datetime
from sinaCrawler.items import sinaArticleItem

class sinaCrawler(scrapy.Spider):

    name = 'sinaCrawler'
    start_urls = []
    # get page x's single href and text
    title = "//div[@class='datelist']/ul/a"
    # itera x(get href)
    XnextPagelink = "//div[@id='con02-7']/table/tr[2]/td/div[3]/a[last()]"

    content = "//*[@id='artibody']/p"  # article's content(text)
    date = "//*[@id='wrapOuter']/div/div[4]/span"  # the article's data(date)
    contentFrom = "//*[@id='wrapOuter']/div/div[4]/span/span/a"  # page Y's author(text)
    driver = None

    databasePre = 'sinaArticles'

    def __init__(self,*args,**kwargs):
        super(sinaCrawler,self).__init__(*args,**kwargs)
        self.start_urls = [kwargs.get('start_url')]

        # self.driver = webdriver.Chrome(executable_path=r'E:\liyi\chromedriver')
        # self.driver = webdriver.Firefox()

        self.pre = "http://vip.stock.finance.sina.com.cn/corp/go.php/vCB_AllNewsStock/symbol/"
        self.stockCode = self.getStockCodeFromUrl(self.start_urls[0])  #make sure start_urls  exists
        self.fdonUrl = open("log/doneUrl"+self.stockCode+".done","a+")

        self.XMulTarget = [
            ('title', self.title)
        ]
        self.XSinTarget = []
        self.YMulTarget = []
        self.YSinTarget = [
            ('content', self.content),
            ('date', self.date),
            ('contentFrom', self.contentFrom)
        ]

    def end(self):
        # self.driver.quit()
        self.fdonUrl.close()
        print "finish!"

#######辅助函数#######

    def extracttime(self,s):
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

    def getStockCodeFromUrl(self,url):
        res = re.search(r'.*([s|S][z|h](\w\d+)).*',url)
        if res:
            stockCode = res.group(2) 
            return str(stockCode)   ###only number
        return -1

#######辅助函数#######

# X层工作函数
    def parse(self, response):

        res = re.search(r'.*([s|S][z|h](\w\d+)).*',response.url)
        if res:
            tableName = res.group(2)

        else:
            print(response.url)
            print("no find! ")
            input("no find:")
            return

        st = u"下载x页面 url: "+response.url + u'完成'
        print(st)

        # 爬取X页的多重属性(title's text and href)
        for name, target in self.XMulTarget:

            st = "getting %s's text and href" % name
            print(st)
            titleItems = response.xpath(target)
            for item in titleItems:  #get title and href
                article = sinaArticleItem()
                article['stockTable'] = tableName
                title = item.xpath('./text()').extract()
                Yhref = item.xpath('./@href').extract()

                print(Yhref)
                fullYurl = response.urljoin(Yhref[0])
                st = title[0] +'\n' + Yhref[0]
                print(st)

                print('request Y href %s' %fullYurl)

                article['title'] = title[0]
                article['url'] = fullYurl
                yield scrapy.Request(fullYurl,callback=self.parseY,meta={'article':article}, dont_filter=True)

        self.fdonUrl.write(response.url+'\n')
        XnextPageElem = response.xpath(self.XnextPagelink)
        if XnextPageElem :
            XnextPagehref = XnextPageElem.xpath('./@href').extract()[0]
            XnextText = XnextPageElem.xpath('./text()').extract()[0]
            fullUrl = XnextPagehref
            # input("x next page:")
            if XnextText.find(u'下一页') == -1:
                return
            else:
                # input('nextpage:')
                yield scrapy.Request(fullUrl,callback=self.parse,dont_filter=True)

# Y层工作函数
    def parseY(self, response):

        st = u"下载y页面 url: "+response.url + u'完成'+'\n'
        print(u"下载y页面 url: "+response.url + u'完成')

        article = response.meta['article']

        # print('bf:')
        # print('response_url:' + '\n' + response.url)
        # print("title:" + '\n' + article['title'])
        # print("article_url:" + '\n' + article['url'])

        # input("bf:")

        for name, target in self.YSinTarget:
            itemcontent = response.xpath(target+'/text()').extract()
            text = ""
            if itemcontent != []:
                for every in itemcontent:
                    text += every

            if name == 'date':
                # print("date: " ,text, itemcontent,itemcontent == [],text == "")
                if itemcontent == []:
                    text = response.xpath('//*[@id="pub_date"]' + '/text()').extract()
                    if text != [] and len(text) > 0:
                        text = text[0]
                
                Date,Time = self.extracttime(text)
                article['date'] = Date
                article['time'] = Time
                continue

            if name == 'contentFrom' and text == "":
                text = response.xpath('//*[@id="media_name"]/a/text()').extract()
                if text != [] and len(text) > 0:
                    text = text[0]

            article[name] = text

        yield article

