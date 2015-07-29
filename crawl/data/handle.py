import pickle,re,pprint

stockCode = []

f = open("namelist(sina).txt","r+")
f.readline()
for ev in f.readlines():
	res = re.search('.*([s|S].(\w\d+)).*',ev)
	if res:
		st = res.group(1)
		stockCode.append((res.group(1),res.group(2)))
f.close()
f = open("namelist(sina).pickle","wb+")
pickle.dump(stockCode,f)
f.close()
f = open("namelist(sina).pickle","rb")
new = pickle.load(f)
pprint.pprint(new)