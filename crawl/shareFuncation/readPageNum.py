import os,re,subprocess,sys
from selenium import webdriver
from pprint import pprint

def getSingleNum(url,xpath,driver):
	print(url)
	driver.get(url)
	driver.implicitly_wait(5)
	pageNum = driver.find_elements_by_xpath(xpath)
	if pageNum == None or len(pageNum) == 1:
		# driver.close()
		return 1
	else:
		print(pageNum[-2].text)
		# driver.close()
		return int(pageNum[-2].text)


def getPageNum(xpath,pre,stockNumbers,location ='pageNum.num'):
	f = open(location,'w+')
	chromePath = r'E:\liyi\chromedriver.exe'
	driver = webdriver.Chrome(executable_path=chromePath)
	ans = {}
	for ev in stockNumbers:
		res = re.search('.*([s|S].(\w\d+)).*',ev)
		if res:
			st = res.group(1)
			url = pre + st
			num = getSingleNum(url,xpath,driver)
			if num == -1:
				print("no find element in %s" %ev)
				continue
			f.write(url+","+st+","+str(num)+'\n')
			ans[st]=num
		else:
			print('not find stockNumber in %s'%ev)

	f.close()
	return ans



