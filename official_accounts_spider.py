#encoding=utf-8
from random import choice
import requests
from bs4 import BeautifulSoup
import bs4 #不推荐写法
import re
# import request_ip
import urllib.request
import urllib.error
import simplejson
import http.cookiejar
import pymysql  
import types  
import json

class OfficialAccounts:
    def __init__(self, url=False):
        #获取随机IP
        # self._host = request_ip.RequestIP().getIP()
        self._url = url if url else 'http://www.jiweixin168.com'
        self._headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
        }
        
        #设置cookie
        self.cookie_filename = 'cookie.txt'
        self.cookie = http.cookiejar.MozillaCookieJar(self.cookie_filename)
        self.handler = urllib.request.HTTPCookieProcessor(self.cookie)
        self.opener = urllib.request.build_opener(self.handler)

        self.official_accounts_array = []

        #连接数据库执行数据库操作
        self.db=pymysql.connect(host="localhost",user="alihanniba",charset="utf8",password="77558@Mysql",db="wxpn");  
        self.cursor=self.db.cursor() 
       
    def get_index_page(self):
        request = urllib.request.Request(self._url, headers = self._headers)
        response = self.opener.open(request)
        content = response.read().decode('UTF-8')
        # content = response.read()
        # 保存cookie到cookie.txt中,  ### 其实不用
        self.cookie.save(ignore_discard=True, ignore_expires=True)  
        #以html解析格式打开
        soup = bs4.BeautifulSoup(content,"html.parser")
        # f = open("jiweixin.html", "wb")
        # f.write(content)
        # f.close;
        sub_nav_ul = soup.find_all("ul", class_ = "sub_nav_ul")
        catalog = sub_nav_ul[0].find_all("li")
        for item in catalog:
            tag_a = item.find_all("a")
            self.cursor.execute('INSERT INTO official_accounts_categories (name) VALUES (%s)', tag_a[0].string)
            self.db.commit() 
            self.cursor.execute('select LAST_INSERT_ID()')
            last_id = self.cursor.fetchone()
            category_id = last_id[0]
            # self.db.close()
            # self.cursor.close()
            for index, content in enumerate(tag_a):
                if index > 0: 
                    sub_database_data = (content.string, int(category_id))
                    self.cursor.execute('INSERT INTO official_accounts_subcategories (name, parent_id) VALUES (%s, %s)', sub_database_data)
                    self.db.commit() 
                    self.cursor.execute('select LAST_INSERT_ID()')
                    sub_last_id = self.cursor.fetchone()
                    subcategory_id = int(sub_last_id[0])
                    # self.db.close()
                    # self.cursor.close()
                    subcategory_url = self._url + content['href']
                    self.get_subcategories(subcategory_url, subcategory_id)
                    return
                # print(subcategory_url)

    def get_subcategories(self, url, parent_id):
        request = urllib.request.Request(url, headers = self._headers)
        response = self.opener.open(request)
        content = response.read().decode('UTF-8')
        # content = response.read()
        # f = open("subcategory.html", "wb")
        # f.write(content)
        # f.close;
        soup = bs4.BeautifulSoup(content,"html.parser")
        sub_nav_ul = soup.find_all("div", class_ = "newslist")
        catalog = sub_nav_ul[0].find_all("dt")

        #获取页码数据，抓取下一页
        sub_page_div = soup.find_all("div", class_ = "page")
        #当前页码数
        current = sub_page_div[0].find_all('span', class_ = "current")[0].string
        
        #最后一个a标签
        tag_a_array = sub_page_div[0].find_all('a')
        
        tag_a_last = tag_a_array[len(tag_a_array) - 1].string
        print(tag_a_last)
        return
        
        #重置数据组装
        self.official_accounts_array = []
        
        for item in catalog:
            tag_a = item.find_all("a")
            thirdcategory_url = self._url + tag_a[0]['href']
            self.get_thirdcategories(thirdcategory_url, parent_id)
        self.cursor.executemany('INSERT INTO official_accounts_thirdcategories (name, wechat_id, attention_count, address, include_time, parent_id, descriptions, qrcode, wechat_link, background_cover) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', self.official_accounts_array)
        self.db.commit() 
        print('----------第一页插库进行中...----------------')
        self.db.close()
        self.cursor.close()
        print('----------第一页插库成功----------------')
        #抓取完一页后睡眠一秒
        sleep(1000)

        return
    
    def get_thirdcategories(self, url, parent_id):
        request = urllib.request.Request(url, headers = self._headers)
        response = self.opener.open(request)
        content = response.read().decode('UTF-8')
        # content = response.read()
        # f = open("thirdcategory.html", "wb")
        # f.write(content)
        # f.close;
        soup = bs4.BeautifulSoup(content,"html.parser")

        #获取公众号主体信息
        sub_nav_ul = soup.find_all("div", class_ = "newsinfo")

        #获取公众号二维码
        try:
            content_img = sub_nav_ul[0].find_all("div", class_ = "qucode_img")
            tag_img = content_img[0].find_all("img")
        except SyntaxError:
            pass

        #获取公众号名称
        try:
            tag_h1 = sub_nav_ul[0].find_all("h1", class_ = "tit_show")
        except SyntaxError:
            pass

        #获取公众号其他信息
        try:
            tag_tit_bot = sub_nav_ul[0].find_all("div", class_ = "tit_bot")
            tag_lis = (tag_tit_bot[0].find_all('li'))
        except SyntaxError:
            pass

        #获取微信号
        try:
            wechat_id = tag_lis[0].find_all('strong')[0].string or ''
        except SyntaxError:
            wechat_id = ''

        #获取关注度
        try:
            attention = re.findall(r"(\d+)", str(tag_lis[2]))
            attention_count = attention[0]
        except SyntaxError:
            attention_count = 0

        #获取所在地区
        try:
            chinese_word = re.compile(u"[\u4e00-\u9fa5]+") 
            address_array = re.findall(chinese_word, str(tag_lis[4]))
            address = address_array[1]
        except SyntaxError:
            address = ''
        

        #获取收录时间
        try:
            include_time_array = re.findall(r"(\d+)", str(tag_lis[5]))
            include_time = include_time_array[0] + '-' + include_time_array[1] + '-' + include_time_array[2]
        except SyntaxError:
            include_time = ''
        
        #获取二维码
        try:
            qrcode = tag_img[0]['src']
        except SyntaxError:
            qrcode = ''

        #获取微信名
        try:
            name = tag_h1[0].string
        except SyntaxError:
            name = ''

        #获取微信介绍
        try:
            sub_description_array = soup.find_all("div", class_ = "view view_c")
            sub_description_div = sub_description_array[0].find_all('div')
        except SyntaxError:
            pass
        
        #获取背景头像
        try:
            background_cover = sub_description_div[0].find_all('img')[0]['src']
        except SyntaxError:
            background_cover = ''

        #获取介绍
        try:
            descriptions = sub_description_div[1].string
        except SyntaxError:
            descriptions = ''
        
        #获取微信公众号链接
        try:
            wechat_link = sub_description_div[2].find_all('a')[0]['href'] or ''
            wechat_link = re.search('mp.weixin.qq.com', wechat_link) or ''
        except IndexError:
            wechat_link = ''
        print('微信名--------------' + name)
        print('微信号--------------' + wechat_id)
        print('关注度--------------' + attention_count)
        print('所在地区------------' + address)
        print('收录时间------------' + include_time)
        print('外键ID-------------' + str(parent_id))
        print('介绍---------------' + descriptions)
        print('二维码-------------' + qrcode)
        print('公众号链接----------' + wechat_link)
        print('背景头像------------' + background_cover)
        #组装数据
        one_account_data = (name, wechat_id, attention_count, address, include_time, parent_id, descriptions, qrcode, wechat_link, background_cover)
        self.official_accounts_array.append(one_account_data)
        print('------------------'+ name +'  组装完成   ------------------------')
        
        

official_accounts = OfficialAccounts()
official_accounts.get_index_page()