# -*- encoding: utf-8 -*-
#encoding=utf-8

import os,subprocess,re,sys,pickle
import codecs,time
from pprint import pprint
projectPath = r"E:\liyi\stockAnaly\crawl"
sys.path.append(projectPath)
from shareFuncation.readPageNum import getPageNum,getSingleNum

print(os.path.realpath(__file__))
os.chdir(os.path.dirname(os.path.realpath(__file__) ) )
# print(os.getcwd())
f = open(r"..\data\namelist(sina).pickle","rb")
stockNumbersAll = pickle.load(f)
xpath = "//*[@id='blk_list_02']/div/p/a"
os.chdir(r"..\data")
# print(os.getcwd())

pre = "http://guba.sina.com.cn/?s=bar&name="
f = open("bbsPageNum.num","r")
totalPages = {}
for ev in f.readlines():
	s = ev.split(":")
	print(s)
	totalPages[ s[2] ] = int(s[3])

# totalPages = getPageNum(xpath,pre,[ev[0] for ev in stockNumbersAll] )

for stockNumber in stockNumbersAll:
	st = stockNumber[0]
	url = pre + st
	stockCode = stockNumber[1]
	fstdout = codecs.open("..\sinabbsCrawler\log\out"+st+".out" ,"w","utf-8")
	fstderr = codecs.open("..\sinabbsCrawler\log\err"+st+".err","w","utf-8")
	totalPage = totalPages[st]
	# print(totalPage)
	doneUrls=0
	trytimes = 0
	# print(os.getcwd())
	os.chdir('..\sinabbsCrawler')
	print(os.getcwd())
	f = open(r"log\doneUrl"+stockCode+".done","w").close()
	while(doneUrls < totalPage):
		trytimes += 1
		print("trytimes:",trytimes,"  doneUrls: ", doneUrls, "  totalPage:",totalPage,"stock: ", stockCode)
		command = 'scrapy crawl sinabbsCrawler -a start_url=%s' %url
		p = subprocess.Popen(command,stdout=fstdout,stderr = fstderr)
		p.communicate()
		returncode = p.returncode
		# print("helel",stockCode)
		f = open(r"log\doneUrl"+stockCode+".done","r+")
		tem = f.readlines()
		url = tem[-1]
		print(len(tem))
		doneUrls = len(tem)
		f.close()
		print("doneUrls: ",doneUrls, " url: ",url)
	fstdout.close()
	fstderr.close()
	# input("returncode:")

