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
            for index, content in enumerate(tag_a):
                # self.cursor.execute('insert into official_accounts_categories (name) values (%s)', content.string)
                # self.db.commit() 
                # self.cursor.execute('select LAST_INSERT_ID()')
                # last_id = self.cursor.fetchone()
                # category_id = last_id[0]
                # self.db.close()
                # self.cursor.close()
                if index > 0: 
                    subcategory_url = self._url + content['href']
                    print(subcategory_url)
                    self.get_subcategories(subcategory_url)
                    return
                # print(subcategory_url)

    def get_subcategories(self, url):
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
        for item in catalog:
            tag_a = item.find_all("a")
            thirdcategory_url = self._url + tag_a[0]['href']
            self.get_thirdcategories(thirdcategory_url)
            print(thirdcategory_url)
            return
    
    def get_thirdcategories(self, url):
        request = urllib.request.Request(url, headers = self._headers)
        response = self.opener.open(request)
        content = response.read().decode('UTF-8')
        # content = response.read()
        # f = open("thirdcategory.html", "wb")
        # f.write(content)
        # f.close;
        soup = bs4.BeautifulSoup(content,"html.parser")
        sub_nav_ul = soup.find_all("div", class_ = "newsinfo")
        content_img = sub_nav_ul[0].find_all("div", class_ = "qucode_img")
        tag_img = content_img[0].find_all("img")
        tag_h1 = sub_nav_ul[0].find_all("h1", class_ = "tit_show")
        cover_url = tag_img[0]['src']
        name = tag_h1[0].string
        print(cover_url)
        print(name)
        return
        
        

official_accounts = OfficialAccounts()
official_accounts.get_index_page()