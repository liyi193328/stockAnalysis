# encoding=utf-8

import scrapy,os,re,datetime,time
from sinabbsCrawler.items import sinabbsPost,sinabbsReply
from pprint import pprint
from marionette import Marionette
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date,time,datetime,timedelta
from scrapy.shell import inspect_response

class sinabbsCrawler(scrapy.Spider): 
    name = 'sinabbsCrawler' 
    start_urls = [
    ]

    Xtitle = "//*[@id='blk_list_02']/table/tbody/tr"

    Xauthor = "//div[@class='articleh']/span[4]/a"
    Xnextlink = "//*[@id='blk_list_02']/div/p/a[last()]" 

    XtoYlink = "//*[@id='blk_list_02']/table/tbody/tr/td[3]/a"

    Ytitle = "//*[@id='thread']/div[2]/h4" 
    Ycontent = "//*[@id='thread']/div[2]/div[1]"
    Ydate = "//*[@id='thread']/div[2]/div[2]/div[1]/span"

    YcommentItem = "//div[@class='item_list clearfix']/div[@class='il_txt']"

    YcommentUser = "./span" 
    YcommentContent = "./p"
    YcommentDate = "./div/div[1]/span"

    YnextPage = "//div[@class='repost_list']/p/a[last()]"
    pre = "http://guba.sina.com.cn/?s=bar&name="

    def __init__(self,*args,**kwargs):
        super(sinabbsCrawler,self).__init__(*args,**kwargs)
        self.start_urls =  [kwargs.get('start_url')]

        # self.driver = webdriver.Chrome(executable_path=r'E:\liyi\chromedriver')
        # self.driverY = webdriver.Chrome(executable_path=r'E:\liyi\chromedriver')
        # self.driverZ = webdriver.Chrome(executable_path=r'E:\liyi\chromedriver')

        # self.driver = webdriver.Firefox()
        self.XMulTarget = [ ("clickNum","./td[1]/span"),
                            ("replyNum","./td[2]/span"),
                            ("title","./td[3]/a"),
                            ("author","./td[4]/div"),
                        ]

        self.XSinTarget = []
        self.YMulTarget = [
            ('commentUser',self.YcommentUser),
            ('commentContent',self.YcommentContent),
            ('commentDate',self.YcommentDate)
        ]

        self.YSinTarget = [
            ('title',self.Ytitle),
            ('content', self.Ycontent),
            ('date', self.Ydate)
        ]
        self.stockCode = self.getStockCodeFromUrl(self.start_urls[0])  #make sure start_urls  exists
        self.fdonUrl = open("log/doneUrl"+str(self.stockCode)+".done","a+")

    def end(self):
        # self.driver.quit()
        self.fdonUrl.close()
        print "finish!"

#######辅助函数#######

    def extracttime(self,s,thatYear): #当s中缺失year值时，就用thatYear替换
        s = s.strip()
        if s:
            if s.find(u'今天') != -1:
                Date = datetime.today().date()
                res = re.search(r'今天\D*(?P<hour>\d+):(?P<minute>\d+)',s.encode('utf-8'))
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
                        year = thatYear
                    if month == None:
                        month = datetime.today().date().month
                    if day == None:
                        day = datetime.today().date().month
                    try:
                        return date(int(year),int(month),int(day)),time(0,0,0)
                    except:
                        pass

            res = re.search(r'((?P<year>\d+)年)?(?P<month>\d+)月(?P<day>\d+)日\D*(?P<hour>\d+):(?P<minute>\d+).*', s.encode('utf8'))
            if res:
                year = res.group('year')
                month = res.group('month')
                day = res.group('day')
                hour = res.group('hour')
                minute = res.group('minute')
                if year == None:
                    year = thatYear
                if hour == None:
                    hour = 0
                if minute == None:
                    minute = 0
            try:
                Date = date(int(year),int(month),int(day))
                Time = time(hour=int(hour),minute = int(minute))
                return Date,Time
            except:
                pass
        return date(1,1,1),time(0,0,0)  

    def getStockCodeFromUrl(self,url):
        res = re.search(r'.*([s|S][z|h](\w\d+)).*',url)
        if res:
            stockCode = res.group(2) 
            return str(stockCode)   ###only number
        return -1

# X层工作函数
    def parse(self, response):

        st = u"下载x页面 url: "+response.url + u'完成'
        print(st)

        # self.driver.get(response.url)

        res = re.search(r'.*([s|S][z|h](\w\d+)).*',response.url)
        if res:
            tableName = res.group(2)

        else:
            print(response.url)
            print("no find tablename in url! ")
            # input("no find:")
            return
        #获取X页的标题和href
        cnt = 0
        for item in response.xpath(self.Xtitle):
            cnt += 1
            if cnt == 1:
                continue  #去掉第一行

            postItem = sinabbsPost()  #declare item for pipline of post
            postItem['stockTable'] = tableName
            fullYurl = None

            for name,singleItemXpath in self.XMulTarget:
                texts =  item.xpath(singleItemXpath+"/text()").extract()
                text = ""
                for ev in texts:
                    text += ev

                postItem[name] = text

                if name == 'title':
                    Yurl = item.xpath(singleItemXpath+"/@href").extract()
                    fullYurl = response.urljoin(Yurl[0])

                    postItem['url'] = fullYurl  

                    # st = u'产生Y页面请求: ' + fullYurl
                    # print(st)

            yield scrapy.Request(fullYurl,callback=self.parseY,meta= {'item':postItem},dont_filter=True)

        self.fdonUrl.write(response.url+'\n')
        # self.driver.get(response.url)
        # # XnextPageElem = self.driver.find_element_by_xpath(self.Xnextlink)
        # XnextPageElem = self.findElementByselenium(self.Xnextlink)
        # print(XnextPageElem.get_attribute('href'))
        # time.sleep(4)
        # # input("XnextPageElem:")
        # if XnextPageElem != None:
        #     XnextPagehref = XnextPageElem.get_attribute('href')
        #     text = XnextPageElem.text
        #     if text.find(u'页') != -1:
        #         XfullUrl = response.urljoin(XnextPagehref)
        #         st = u'产生x页面请求: ' + XfullUrl
        #         print(st)
        #         # input("st:")
        #         yield scrapy.Request(XfullUrl,callback=self.parse,dont_filter=True)

        XnextPagehref = response.xpath(self.Xnextlink + '/@href').extract()[0]
        text = response.xpath(self.Xnextlink+'/text()').extract()[0]
        if text.find(u'页') != -1:
            fullNextUrl = response.urljoin(XnextPagehref)
            print(fullNextUrl)
            # input("st:")
            yield scrapy.Request(fullNextUrl,callback=self.parse,dont_filter=True)


# Y层工作函数
    def parseY(self, response):

        st = u"下载y页面 url: "+response.url + u'完成'+'\n'
        print(u"下载y页面 url: "+response.url + u'完成')

        postItem = response.meta['item']

        for name, target in self.YSinTarget:  #帖子内容
            itemcontents = response.xpath(target+'/text()').extract()
            text = ""
            if itemcontents != None:
                for item in itemcontents:
                    text += item

            if name == 'date':
                Date,Time = self.extracttime(text,2015) #目前的年份
                postItem['date'] = Date
                postItem['time'] = Time

            else:
                postItem[name] = text

        yield postItem

        if int( postItem['replyNum'] ) > 0:
            print(postItem['url'], postItem['replyNum'])
            st = u'产生回复页%s请求' %postItem['url']
            print(st)

            yield scrapy.Request(postItem['url'],callback=self.parseComment,
                        meta = {'stockTable': postItem['stockTable'],'year':postItem['date'].year},
                        dont_filter=True)

    def parseComment(self,response):  #爬取回复内容

        print(u'下载回复页面%s完成'%response.url)
        
        commentItem = sinabbsReply()
        commentItem['url'] = response.url #被回复的帖子的url
        commentItem['stockTable'] = response.meta['stockTable']
        commentyear = int(response.meta['year'])  #帖子发表年
        thisyear = datetime.today().date().year  #今年
        # self.driver.get(response.url)
        # self.driver.implicitly_wait(5) # seconds

        for commentRootXpath in response.xpath(self.YcommentItem):
            for name,target in self.YMulTarget:
                itemcontents = commentRootXpath.xpath(target+'/text()').extract()
                if name == 'commentUser' and itemcontents == []:
                    itemcontents = commentRootXpath.xpath(target+'/a/text()').extract() #有些用户是链接
                
                if itemcontents == []:
                    continue
                if type(itemcontents) == list:
                    text = itemcontents[0]
                else:
                    text = itemcontents
                    
                if name == 'commentDate':
                    print(text)
                    Date,Time = self.extracttime(text,commentyear)
                    commentItem['commentDate'] = Date
                else:
                    commentItem[name] = text
            yield commentItem
        
        lastpage = response.xpath(self.YnextPage)
        if lastpage == None or lastpage == []:
            return
        text = ""
        href = ""
        if type(lastpage) == list:
            text = lastpage[0].xpath('./text()').extract()[0]
            href = lastpage[0].xpath('./@href').extract()[0]
        else:
            text = lastpage.xpath('./text()').extract()[0]
            href = lastpage.xpath('./@href').extract()[0]

        if text.find(u'页') != -1:
            fullNextUrl = response.urljoin(href)
            print("fullNextUrl: ",fullNextUrl)
            # input('page:')
            yield scrapy.Request(fullNextUrl,callback=self.parseComment,meta = {'stockTable':commentItem['stockTable']}, dont_filter=True)

    def findElementByselenium(self,xpath,waittime=5):

        for trytimes in range(0,4):
            if trytimes > 2:
                print('trytimes: %d' %trytimes)
            try:
                elem = WebDriverWait(self.driver,waittime).until(
                    EC.presence_of_element_located( (By.XPATH, xpath) )
                    )
                return elem
            except NoSuchElementException:
                print("NoSuchElementException!")
            except StaleElementReferenceException:
                print "StaleElementReferenceException!"

