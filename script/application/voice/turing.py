#encoding:utf-8
 
import urllib.request
import json  
 
# 调用图灵接口的类
class turing(object):
	"""传入人说的话,返回电脑的回答"""
	# init the turing
	def __init__(self):
		self._key = 'a3d6301b851abb919f1e347fc8c49cc4'

	# 获取网页内容,post请求
	def getHtml(self, url):  
		page = urllib.request.urlopen(url)  
		html = page.read()  
		return html

	# interactive with human
	def interactive(self, speech_content):
		self._api = 'http://www.tuling123.com/openapi/api?key=' + self._key + '&info='  
		self._info = str(speech_content.encode('utf-8'))   # 转为字符串
		request = self._api + self._info
		response = self.getHtml(request)
		# print('response', response)
		rep = str(response, encoding = "utf-8")
		# print('rep=', rep)
		dic_json = json.loads(rep)  
		# print ('robot: ' + dic_json['text'] ) 
		return dic_json['text']

if __name__ == '__main__': 
	understand = turing() #初始化图灵机器人类
	while True:
		question = input('human:')
		content = understand.interactive(question)
		print('robot:', content)