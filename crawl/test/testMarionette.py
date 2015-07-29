#encoding=utf-8
from marionette import Marionette

client = Marionette('localhost', port=2828)
client.start_session()
client.navigate('http://finance.sina.com.cn/stock/s/20150714/070922678344.shtml')#访问当前访问的网址
elem = client.find_element('xpath',"//*[@id='wrapOuter']/div/div[4]/span")
print(elem.text)