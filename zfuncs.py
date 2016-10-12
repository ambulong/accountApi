#coding:utf-8
from selenium.webdriver.common.by import By
import sys   
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入   
sys.setdefaultencoding('utf-8')

#获取用来判断是否已注册字符串的对象，遍历标签，速度慢
def z_get_element_by_key_exists(driver):
	eles = driver.find_elements(By.XPATH, '//a | //span | //li | //b | //font | //div')
	#eles = driver.find_elements(By.XPATH, '//span')
	for line in open("./keys/exists.key"):
		line = line.strip('\n')
		for ele in eles:
			if ele.get_attribute("innerHTML").find('<')!=-1 or ele.get_attribute("innerHTML")=='':#如果包含html标签则无视掉
				continue
			else:
				#print ele.get_attribute("outerHTML")
				if(ele.get_attribute("innerHTML").find(line)!=-1):
					return ele
	return False

#获取用来判断是否已注册字符串，直接搜索文本，速度快，准确性低
def z_get_isexists_by_key_exists(driver):
	bodyhtml = driver.find_element(By.XPATH, '//body').get_attribute("innerHTML")
	for line in open("./keys/exists.key"):
		line = line.strip('\n')
		if(bodyhtml.find(line)!=-1):
			print line
			return 'Found'
	return False

#获取手机的input对象，如果失败返回False
def z_get_input_element_by_key_phone(driver):
	input_boxes = driver.find_elements(By.XPATH, "//input[@type='text']")
	for line in open("./keys/phone.key"):
		line = line.strip('\n')
		for element in input_boxes:#先查找name
			if element.get_attribute('name').find(line) != -1 and element.is_displayed(): #需要判断输入框用户是否可见
				return element
		for element in input_boxes:#查找id
			if element.get_attribute('id').find(line) != -1 and element.is_displayed(): 
				#print element.get_attribute('id')
				return element
	return False

#获取邮箱的input对象，如果失败返回False
def z_get_input_element_by_key_email(driver):
	input_boxes = driver.find_elements(By.XPATH, "//input[@type='text']")
	for line in open("./keys/email.key"):
		line = line.strip('\n')
		for element in input_boxes:
			if element.get_attribute('name').find(line) != -1: 
				return element
		for element in input_boxes:#查找id
			if element.get_attribute('id').find(line) != -1: 
				return element
	return False

#获取用户名的input对象，如果失败返回False
def z_get_input_element_by_key_username(driver):
	input_boxes = driver.find_elements(By.XPATH, "//input[@type='text']")
	for line in open("./keys/username.key"):
		line = line.strip('\n')
		for element in input_boxes:
			if element.get_attribute('name').find(line) != -1: 
				return element
		for element in input_boxes:#查找id
			if element.get_attribute('id').find(line) != -1: 
				return element
	return False
