from random import choice
import requests
from bs4 import BeautifulSoup
import bs4 #不推荐写法
import re
import request_ip
import urllib.request
import simplejson

class Wechat:
    def __init__(self):
        self._host = request_ip.RequestIP().getIP()
        self._url = 'https://mp.weixin.qq.com/mp/getmasssendmsg?__biz=MzI4MTA2OTA1Mg==&from=1&uin=MjA0NjcxNzUwMA%3D%3D&key=a9d7e7f2647cda56c09277a9e1a47fef133d1a25b4cfd8eeead76f2aed61c6f5355e67e48837ab9a3dad64409f91ed579ef27c1997432f18a6784cdbfbbb867e8e6586c247e49dd4865212ca4d7271e9&devicetype=iMac+MacBookPro12%2C1+OSX+OSX+10.12.3+build(16D32)&version=12010310&lang=zh_CN&nettype=WIFI&ascene=0&fontScale=100&pass_ticket=9VNc%2BuPHO2Yfrgz2GS%2BZ5LA28LMVeV9fUaLHjtjIJZnP4deavqs3KHmdZ%2F%2Bax1Oo#wechat_webview_type=1'
        self._headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
        }
        self.uin = ''
        self.key = ''
        self.frommsgid = ''
        self.count = 10
        self.f_uin = ''
        self.pass_ticket = ''
        self.wxtoken = ''
        self.x5 = 0
    
    def get_articles(self):
        # r = requests.get(self._url, headers = self._headers)
        # soup = bs4.BeautifulSoup(r.text,"html.parser")
        # htmlFile = open(r"page1.html", "r")
        # content = htmlFile.read()
        soup = bs4.BeautifulSoup(open("page1.html"), "lxml")
        # minMsgId = soup.script.find_all("script", limit=40)
        # print(soup.prettify()) # 格式化输出
        script = soup.body.find_all("script")
        data = script[-1]
        uin = re.findall(r'uin = "(\S+)"', str(data))
        key = re.findall(r'key = "(\S+)"', str(data))
        msg_list = re.findall(r'msgList = {(.*?)};', str(data),re.S)
        # print(uin)
        # print(key)
        # print(msg_list[0])
        msg_list_str = "{" + msg_list[0] + "}"
        #转为字典
        msg_list_dict = simplejson.loads(msg_list_str)
        # for key, value in msg_list_dict.iteritems():
        app_msg_list = msg_list_dict.get("list")
        for i in app_msg_list:
            print(i.get("app_msg_ext_info"))
            return;
        # print(msg_list_dict.get("list"))

wechat = Wechat()
wechat.get_articles()