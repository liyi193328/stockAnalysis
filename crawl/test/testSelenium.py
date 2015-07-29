#encoding=utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from marionette import Marionette
from selenium.common.exceptions import NoSuchElementException

import time
# driver = webdriver.PhantomJS(executable_path='/home/liyi193328/phantomjs/bin/phantomjs',service_args=['--ssl-protocol=any'])


YcommentItem = "//*[@id='thread']/div[2]/div[3]/div[4]/div"

YcommentUser = ".//div[@class='il_txt']/span" 
YcommentContent = ".//div[@class='il_txt']/p"
YcommentDate = ".//div[@class='il_txt']/div/div[1]/span"
YnextPage = "//*[@id='thread']/div[2]/div[3]/div[4]/p/a"

YMulTarget = [
    ('commentUser',YcommentUser),
    ('commentContent',YcommentContent),
    ('commentDate',YcommentDate)
]

driver = webdriver.Chrome(executable_path='C:\project\liyi\stockAnaly\crawl\chromedriver')
# driver = webdriver.Firefox()
driver.implicitly_wait(5)
driver.get("http://guba.sina.com.cn/?s=thread&tid=141044&bid=567")
print(driver.title)
elem = driver.find_element_by_xpath("//*[@id='thread']/div[2]/div[3]/div[4]/div/div[2]/div/div[1]/span")
print(elem.get_attribute("innerHTML"))

for commentRootXpath in driver.find_elements_by_xpath(YcommentItem):
    # print(commentRootXpath.get_attribute("innerHTML"))
    for name,target in YMulTarget:
        itemcontents = commentRootXpath.find_element_by_xpath(target).text
        print(name,itemcontents)
        text = itemcontents
        print(text)

page = driver.find_elements_by_xpath(YnextPage)
if(len(page) == 0):pass
Ynexttext = page[len(page)-1].text
print(Ynexttext)
if Ynexttext.find(u'页') == -1:
    print('no find ye')
    pass
else:
    Ynexthref = page[len(page)-1].get_attribute('href')
    print(Ynexthref)
# time.sleep(5)
# driver.get_screenshot_as_file("sinabbs_page2.png")
# print(driver.page_source)
# elem = driver.find_element_by_xpath("//*[@id='artibody']")
# print(elem.text) 
# try:
#     elem = driver.find_element_by_xpath('//*[@id="J_Post_Box_Count"]/a')
#     st = u"获取标题:"+ elem.get_attribute("href")
#     print(st)
# except NoSuchElementException:
#     print u"no find"
# try:
#     element = WebDriverWait(driver, 5).until(
#         EC.presence_of_element_located((By.XPATH,'//*[@id="J_Post_Box_Count"]/a'))
#      )
#     print(element.get_attribute("href"))
#     driver.save_screenshot("sinabbs_page2.png")
# except:
#     input("exe:")
#     driver.quit()


# start_urls = [
#     'http://comment5.news.sina.com.cn/comment/skin/default.html?channel=cj&newsid=31-1-22583013']

# ZcommentRootXpath = "//*[@id='J_Comment_List_Latest']"
# ZcommentPageFirst = ZcommentRootXpath+"/div[1]"  

# ZcommentItem = ZcommentPageFirst+"/div[@class='comment_item']"
# Zusername = ".//div/div[2]/div[1]/div/span[1]/a"
# Zuserarea = ".//div/div[2]/div[1]/div/span[2]"
# Zcommentcontent = ".//div/div[2]/div[3]/div[1]"
# Zcommentdate = ".//div/div[2]/div[3]/div[2]/span[1]"


#     # 用selenium 控制chrome，模拟操作
# driver = webdriver.Chrome(executable_path='/home/liyi193328/software/chromedriver')
# # driver = webdriver.Firefox()

# f = open('sina.txt', 'w')  # 用于存储测试输出内容的文本文件

# ZMulTarget = [
#         ('Zusername', Zusername),
#         ('Zuserarea', Zuserarea),
#         ('Zcommentcontent', Zcommentcontent),
#         ('Zcommentdate',Zcommentdate)
#     ]
# ZSinTarget = []
# Zurl = start_urls[0]
# driver.get(Zurl)

# st = "下载Z评论页面"+Zurl+"完成"
# print("下载Z评论页面"+Zurl+"完成")
# f.write(st)
# f.flush()

# items = list(driver.find_elements_by_xpath(ZcommentItem))
# print(len(items))
# input("len:")
# for commentItems in items:
#     for name, target in ZMulTarget:
#         item = commentItems.find_element_by_xpath(target)
#         allText = item.text
#         text = ""
#         for every in allText:
#             text += every
#         print name+':\n'+text
#         # input("Zcontent:")
#         f.write(text.encode('utf8')+'\n')
#         f.flush
# driver.close()
