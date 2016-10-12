#自动化爬取用户名/手机/邮箱是否已经注册接口的工具

使用的是python+selenium+chromedriver

#安装

pip install selenium

下载chromedriver. https://sites.google.com/a/chromium.org/chromedriver/downloads

#文件描述

email.key: 表单项关键字，用于查找填写邮箱的表单项
phone.key: 表单项关键字，用于查找填写手机号的表单项
username.key: 表单项关键字，用于查找填写用户名的表单项
findpass.key: 找回密码链接关键字，用于查找找回密码链接
login.key: 登录链接关键字，用于查找登录链接
register.key: 注册链接关键字，用户查找注册链接


# accountApi
