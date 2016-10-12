#coding:utf-8

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from browsermobproxy import Server
import zfuncs
import time, sys, string, random, json, requests

path_to_browsermob_proxy = "/home/ambulong/browsermob-proxy-2.1.2/bin/browsermob-proxy"
path_to_chromedriver = "/home/ambulong/chromedriver"

class AccountApi(object):
	driver = None
	proxy = None
	server = None
	canFoundInText = False
	
	def __init__(self, url):
		print "ready to get api: "+url
		if self.url_available(url) != False:
			self.start_driver(url)
		
			#判断“已存在”关键字是否在网页代码中存在
			isFoundExists = zfuncs.z_get_isexists_by_key_exists(self.driver)
		
			#如果已存在关键字则详细查找
			if isFoundExists!=False:
				self.canFoundInText = True
				isFoundExists = zfuncs.z_get_element_by_key_exists(self.driver)
		
			#原网页存在关键字会导致误报
			if isFoundExists!=False:
				print "原网页存在关键字"
				self.do_nothing()
		else:
			print url + " is unavailable"
			self.do_nothing()
				
	def do_nothing(self):
		return
		
	def start_driver(self, url):
		self.server = Server(path_to_browsermob_proxy)
		self.server.start()
		self.proxy = self.server.create_proxy()
		
		#设置代理
		chrome_options = webdriver.ChromeOptions()
		chrome_options.add_argument("--proxy-server={0}".format(self.proxy.proxy))
		
		d = DesiredCapabilities.CHROME
		d['loggingPrefs'] = { 'performance':'ALL' }
		
		try:
			self.driver = webdriver.Chrome(path_to_chromedriver, desired_capabilities=d, chrome_options=chrome_options)
			self.proxy.new_har("zaccapi", options={'captureHeaders': True, 'captureContent': True})
			self.driver.set_page_load_timeout(5)
			self.driver.get(url)
		except:
			try:
				self.driver.find_element_by_css_selector('body').send_keys(Keys.ESCAPE)
			except:
				self.do_nothing()
				
	def do_nothing(self):
		return
	
	#析构函数
	def __del__(self):
		try:
			self.server.stop()
		except:
			self.do_nothing()
		try:
			self.driver.quit()
		except:
			self.do_nothing()
	
	#获取网页标题
	def get_title(self):
		if self.server == None: 
			return False
		return self.driver.title
		
	#测试获取接口
	def get_api_test(self):
		if self.server == None: 
			return False
		print "==username=="
		print self.get_username_api();
		print "==phone=="
		print self.get_phone_api();
		print "==email=="
		print self.get_email_api();
	
	#获取用户名是否存在接口, 返回-1未查找到用户名输入框，返回-2填写后无HTTP请求，返回-3填写测试数据后未发现请求包，返回-4无法抓取已注册请求包（现有测试数据都未注册）
	def get_username_api(self):
		if self.server == None: 
			return False
		element = zfuncs.z_get_input_element_by_key_username(self.driver)#获取用户名输入框
		if element==False:
			print "未查找到用户名输入框"
			return -1
		req_url = self.get_username_api_url(element)#获取请求URL，用于定位请求包
		if req_url==False:
			return -2
		
		#使用常用用户名测试，获取用户存在响应包
		for line in open("./keys/username.value"):
			line = line.strip('\n')
			entry = self.find_entry_by_string(element, line)
			if entry!=False and entry['request']['url'].find(req_url)!=-1:#确认请求包
				#判断是否已注册请求包
				if self.canFoundInText == False:
					is_exist = zfuncs.z_get_isexists_by_key_exists(self.driver)
				else:
					is_exist = zfuncs.z_get_element_by_key_exists(self.driver)
				if is_exist!=False:
					print line+"：发现已注册"
					return entry #返回当前请求包
				else:
					print line+"：未发现已注册"
			else:
				print line+"：未发现请求包"
				return -3
			
		return -4
	
	#获取手机号是否存在接口, 返回-1未查找到用户名输入框，返回-2填写后无HTTP请求，返回-3填写测试数据后未发现请求包，返回-4无法抓取已注册请求包（现有测试数据都未注册）
	def get_phone_api(self):
		if self.server == None: 
			return False
		element = zfuncs.z_get_input_element_by_key_phone(self.driver)#获取手机号码输入框
		if element==False:
			print "未查找到手机号码输入框"
			return -1
		req_url = self.get_phone_api_url(element)#获取请求URL，用于定位请求包
		if req_url==False:
			return -2
		
		#使用常用用户名测试，获取用户存在响应包
		for line in open("./keys/phone.value"):
			line = line.strip('\n')
			entry = self.find_entry_by_string(element, line)
			if entry!=False and entry['request']['url'].find(req_url)!=-1:#确认请求包
				#判断是否已注册请求包
				if self.canFoundInText == False:
					is_exist = zfuncs.z_get_isexists_by_key_exists(self.driver)
				else:
					is_exist = zfuncs.z_get_element_by_key_exists(self.driver)
				if is_exist!=False:
					print line+"：发现已注册"
					return entry #返回当前请求包
				else:
					print line+"：未发现已注册"
			else:
				print line+"：未发现请求包"
				return -3
			
		return -4
	
	#获取邮箱是否存在接口, 返回-1未查找到用户名输入框，返回-2填写后无HTTP请求，返回-3填写测试数据后未发现请求包，返回-4无法抓取已注册请求包（现有测试数据都未注册）
	def get_email_api(self):
		if self.server == None: 
			return False
		element = zfuncs.z_get_input_element_by_key_email(self.driver)#获取邮箱输入框
		if element==False:
			print "未查找到邮箱输入框"
			return -1
		req_url = self.get_email_api_url(element)#获取请求URL，用于定位请求包
		if req_url==False:
			return -2
		
		#使用常用用户名测试，获取用户存在响应包
		for line in open("./keys/email.value"):
			line = line.strip('\n')
			entry = self.find_entry_by_string(element, line)
			if entry!=False and entry['request']['url'].find(req_url)!=-1:#确认请求包
				#判断是否已注册请求包
				if self.canFoundInText == False:
					is_exist = zfuncs.z_get_isexists_by_key_exists(self.driver)
				else:
					is_exist = zfuncs.z_get_element_by_key_exists(self.driver)
				if is_exist!=False:
					print line+"：发现已注册"
					return entry #返回当前请求包
				else:
					print line+"：未发现已注册"
			else:
				print line+"：未发现请求包"
				return -3
			
		return -4
	
	#获取用户名是否存在接口的请求URL
	def get_username_api_url(self, element):
		if self.server == None: 
			return False
		str = 'z'+self.id_generator()#生成测试用户名
		entry = self.find_entry_by_string(element, str)
		
		if entry==False:
			return False
		
		url = entry['request']['url']
		return url.split("?")[0]
	
	#获取手机号是否存在接口的请求URL
	def get_phone_api_url(self, element):
		if self.server == None: 
			return False
		str = '1300'+self.id_generator(7, '0123456789')#生成测试手机号
		entry = self.find_entry_by_string(element, str)
		
		if entry==False:
			return False
		
		url = entry['request']['url']
		return url.split("?")[0]
	
	#获取邮箱是否存在接口的请求URL
	def get_email_api_url(self, element):
		if self.server == None: 
			return False
		str = self.id_generator()+"@qq.com"#生成测试邮箱
		entry = self.find_entry_by_string(element, str)
		
		if entry==False:
			return False
		
		url = entry['request']['url']
		return url.split("?")[0]
	
	#定位请求包位置, element为用来填写内容的input输入框
	def find_entry_by_string(self, element, keystr):
		#获取输入内容后的所有网络请求
		entries = self.get_entries(element, keystr)
		#查找是否有网络请求
		entry = self.find_har_by_string(entries, keystr)
		if entry==False:
			print "未发起网络请求"
			return False
		print "发现填写后会发起网络请求"
		
		return entry
	
	#获取输入内容后的所有网络请求
	def get_entries(self, element, keystr):
		if element==False:#该页未查找到输入用户名的地方
			return False
		if element.get_attribute('name')!='':
			print "Input name: "+element.get_attribute('name')
		if element.get_attribute('id')!='':
			print "Input id: "+element.get_attribute('id')
		print "填写测试字符串："+keystr
		element.send_keys(Keys.CONTROL + "a")
		element.send_keys(keystr)
		element.send_keys(Keys.TAB)
		time.sleep(2)#等待请求结束，页面改变
		return self.proxy.har['log']['entries']
		
	#查找数组中包含关键字的数组项
	def find_har_by_string(self, arr, keystr):
		if type(arr)!=list:
			return False
    		#倒序遍历数组，查找关键字符串
    		for i in range(0, arr.__len__())[::-1]:
			if json.dumps(arr[i]).find(keystr)!=-1:
				return arr[i]
		return False
			
	#获取随机值
	def id_generator(self, size=6, chars=string.ascii_lowercase + string.digits):
		return ''.join(random.choice(chars) for _ in range(size))

	#检查链接是否可用，弃用，误报率高
	def url_available(self, url):
		return True
		try:
			r = requests.head(url, timeout=3)
	    		return r.status_code == 200
	    	except:
	    		return False

if __name__=='__main__':  
    obj = AccountApi('http://www.cndns.com/members/register.aspx')
    obj.get_api_test()
