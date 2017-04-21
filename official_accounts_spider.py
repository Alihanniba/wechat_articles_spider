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

class OfficialAccounts:
    def __init__(self, url=False):
        #获取随机IP
        # self._host = request_ip.RequestIP().getIP()
        self._url = url if url else 'http://www.jiweixin168.com/'
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
        catalog_content = re.compile('')
        ss = catalog[0].find_all("a")
        
        print(ss[0]['href'])
        return soup

    def get_data(self, url):
        request = urllib.request.Request(url, headers = self._headers)
        response = self.opener.open(request)
        content = response.read().decode('UTF-8')
        # content = open("page2.json", "r").read()
       

official_accounts = OfficialAccounts()
official_accounts.get_index_page()