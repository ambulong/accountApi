#coding:utf-8

import getapi
import geturl
import threading, time, sys

site_list = []
lock = 0
thread_nums = 0

for line in open("./site.txt"):
	line = line.strip('\n')
	if line!='':
		site_list.append(line);

class my_thread(threading.Thread): #The timer class is derived from the class threading.Thread  
	def __init__(self, num, interval):  
		threading.Thread.__init__(self)  
		self.thread_num = num  
		self.interval = interval
		self.interruptEvent = threading.Event()
   
	def run(self): #Overwrite run() method, put what you want the thread do here 
        	get_api(self.thread_num, self.interval)
        		

def get_api(num, interval):
	global lock
	global site_list
	global thread_nums
	thread_nums += 1
	try:
		if lock == 0:
			lock = 1
			if len(site_list) <= 0 :
				lock = 0
			site = site_list.pop() #获取最后一个站点，并从数组中移除
			print "Thread "+str(num)+" start: "+site
			lock = 0
			obj_gu = geturl.GetURL(site)
			
			#注册页面
			regurl = obj_gu.get_register_url()
			if regurl!=False:
				print "Found reg url: "+regurl
				obj_aa = getapi.AccountApi(regurl)
				obj_aa.get_api_test()
			
			#登录页面
			loginurl = obj_gu.get_login_url()
			if loginurl != False:
				print "Found login url: "+loginurl
				obj_aa = getapi.AccountApi(loginurl)
				obj_aa.get_api_test()
			
		else:
			time.sleep(interval)
	except:
		lock = 0
	thread_nums -= 1
	print "Thread "+str(num)+" end"
	return
		
def test():
	global thread_nums
	all_thread_num = 0
	while(1):
		if thread_nums<1:#线程数量
			all_thread_num+=1
			thread = my_thread(all_thread_num, 1)
			thread.start()
	return 

if __name__=='__main__':  
    test()  
