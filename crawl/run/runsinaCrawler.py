# -*- encoding: utf-8 -*-
#encoding=utf-8

import os,subprocess,re,sys,pickle,time
import codecs
from pprint import pprint
projectPath = r"E:\liyi\stockAnaly\crawl"
sys.path.append(projectPath)
from shareFuncation.readPageNum import getPageNum,getSingleNum

print(os.path.realpath(__file__))
os.chdir(os.path.dirname(os.path.realpath(__file__) ) )
print(os.getcwd())
f = open(r"..\data\namelist(sina).pickle","rb")
stockNumbersAll = pickle.load(f)
xpath = "//div[@id='con02-7']/table/tr[2]/td/div[3]/a"
os.chdir(r"..\data")
print(os.getcwd())
pre = "http://vip.stock.finance.sina.com.cn/corp/go.php/vCB_AllNewsStock/symbol/"
# f = open("articlePageNum.num","r")
# totalPages = {}
# for ev in f.readlines():
#       s = ev.split(":")
#       print(s)
#       totalPages[ s[2] ] = int(s[3])

for stockNumber in stockNumbersAll:
      st = stockNumber[0]
      url = pre + st + ".phtml"
      stockCode = stockNumber[1]
      print(os.getcwd())
      fstdout = codecs.open("..\sinaCrawler\log\out"+st+".out" ,"w","utf-8")
      fstderr = codecs.open("..\sinaCrawler\log\err"+st+".err","w","utf-8")
      # print(os.getcwd())
      os.chdir('..\sinaCrawler')
      for trytimes in range(0,3):
            trytimes += 1
            print("trytimes:",trytimes,"stock: ", stockCode)
            command = 'scrapy crawl sinaCrawler -a start_url=%s' %url
            p = subprocess.Popen(command,stdout=fstdout,stderr = fstderr)
            p.communicate()
            returncode = p.returncode
            if returncode == 0:
                  break
            f = open(r"log\doneUrl"+stockCode+".done","r+")
            time.sleep(5)
            url = f.readlines()[-1]
            f.close()
            print(" url: ",url)
            # input("xx:")

      fstdout.close()
      fstderr.close()
      # input("returncode:")