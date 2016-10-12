#coding:utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import zfuncs
import time, sys, string, random, json, requests

path_to_chromedriver = "/home/ambulong/chromedriver"

class GetURL(object):
	driver = None
	
	def __init__(self, url):
		try:
			if self.url_available(url) != False:
				self.driver = webdriver.Chrome(path_to_chromedriver)
				self.driver.set_page_load_timeout(5)
				self.driver.get(url)
			else:
				print url + " is unavailable"
		except:
			print url + " is timeout"
			try:
				self.driver.find_element_by_css_selector('body').send_keys(Keys.ESCAPE)
			except:
				self.do_nothing()
				
	def do_nothing(self):
		return
	
	#析构函数
	def __del__(self):
		if self.driver != None:
			self.driver.quit()
		
	#查找注册URL
	def get_register_url(self):
		if self.driver == None:
			return False
		for line in open("./keys/register.key"):
			line = line.strip('\n')
			ele = self.z_find_element_by_partial_link_text(line)
			if ele!=False:
				link = ele.get_attribute('href')
				if link != '':
					return link
			
		return False
	
	#查找登录URL
	def get_login_url(self):
		if self.driver == None:
			return False
		for line in open("./keys/login.key"):
			line = line.strip('\n')
			ele = self.z_find_element_by_partial_link_text(line)
			if ele!=False:
				link = ele.get_attribute('href')
				if link != '':
					return link
			
		return False
	
	#查找找回密码URL
	def get_findpass_url(self):
		if self.driver == None:
			return False
		for line in open("./keys/findpass.key"):
			line = line.strip('\n')
			ele = self.z_find_element_by_partial_link_text(line)
			if ele!=False:
				link = ele.get_attribute('href')
				if link != '':
					return link
			
		return False
	
	#根据关键字获取链接对象
	def z_find_element_by_partial_link_text(self, keystr):
		if self.driver == None:
			return False
		try:
			ele = self.driver.find_element_by_partial_link_text(keystr)
			return ele
		except:
			return False
	
	#检查链接是否可用
	def url_available(self, url):
		try:
			r = requests.head(url, timeout=3)
	    		return r.status_code == 200
	    	except:
	    		return False
    	
