from random import choice
import requests
from bs4 import BeautifulSoup
import bs4 #不推荐写法
import re
import request_ip
import urllib.request
import urllib.error
import simplejson
import http.cookiejar

class Wechat:
    def __init__(self, url):
        #获取随机IP
        self._host = request_ip.RequestIP().getIP()
        # self._url = 'https://mp.weixin.qq.com/mp/getmasssendmsg?__biz=MzI4MTA2OTA1Mg==&from=1&uin=MjA0NjcxNzUwMA%3D%3D&key=a9d7e7f2647cda56c09277a9e1a47fef133d1a25b4cfd8eeead76f2aed61c6f5355e67e48837ab9a3dad64409f91ed579ef27c1997432f18a6784cdbfbbb867e8e6586c247e49dd4865212ca4d7271e9&devicetype=iMac+MacBookPro12%2C1+OSX+OSX+10.12.3+build(16D32)&version=12010310&lang=zh_CN&nettype=WIFI&ascene=0&fontScale=100&pass_ticket=9VNc%2BuPHO2Yfrgz2GS%2BZ5LA28LMVeV9fUaLHjtjIJZnP4deavqs3KHmdZ%2F%2Bax1Oo#wechat_webview_type=1'
        
        self._url = url if url else 'https://mp.weixin.qq.com/mp/getmasssendmsg?__biz=MzI4MTA2OTA1Mg==&from=1&uin=MjA0NjcxNzUwMA%3D%3D&key=c6f43e46893b1d7116614af4b875a6aedfbecb46d2baa3cd4eea49324eeb22f0342a750a2579e661beae17e37c6e28ebf59aea546b7c046f60bff77621d2765453ae30f1606c6f68b2c4a8d61b7f6bb1&devicetype=iOS10.2&version=16050520&lang=en&nettype=WIFI&ascene=7&fontScale=100&pass_ticket=KK1vof%2BLW5ltw%2Bdy9MfflELNzD9uJ%2BYzpe9D%2BdaOLTUqlQpD3o1fVPEltGEqAoTC&wx_header=1'
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

        #下一次请求URL链接参数
        self.start = 'https' + (re.findall(r'https(.*?)&', self._url))[0]
        self.uin = ''
        self.key = ''
        self.f = 'json'
        self.frommsgid = ''
        self.count = '10'
        self.f_uin = ''
        self.pass_ticket = ''
        self.wxtoken = ''
        self.x5 = '0'
        
        #验证是否进行下一次请求
        self.flag = True        
    
    def get_articles_from_first(self):
        # request = urllib.request.Request(self._url, headers = self._headers)
        # response = self.opener.open(request)
        # self.cookie.save(ignore_discard=True, ignore_expires=True)  # 保存cookie到cookie.txt中
        # soup = bs4.BeautifulSoup(response,"html.parser")
        # print(soup)
        # return
        # htmlFile = open(r"page1.html", "r")
        # content = htmlFile.read()
        soup = bs4.BeautifulSoup(open("page1.html"), "lxml")
        minMsgId = soup.script.find_all("script", limit=40)
        # print(soup.prettify()) # 格式化输出
        script = soup.body.find_all("script")
        data = script[-1]
        uin = re.findall(r'uin = "(\S+)"', str(data))
        key = re.findall(r'key = "(\S+)"', str(data))
        self.uin = uin[0] if uin else ''
        self.key = key[0] if key else ''
        msg_list = re.findall(r'msgList = {(.*?)};', str(data),re.S)
        # print(msg_list)
        # return
        # print(self.uin)
        # print(self.key)
        # print(msg_list[0])
        msg_list_str = "{" + msg_list[0] + "}"
        #转为字典
        msg_list_dict = simplejson.loads(msg_list_str)
        # for key, value in msg_list_dict.iteritems():
        app_msg_list = msg_list_dict.get("list")
        # for i in app_msg_list:
        #     print(i.get("app_msg_ext_info"))
        #     return;
        # print(len(app_msg_list))
        if len(app_msg_list) > 9:
            # print(app_msg_list[9])
            #获取构造下次URL的ID
            self.frommsgid = app_msg_list[9].get('comm_msg_info').get('id');
            # print(self.frommsgid)
        f_uin = re.findall(r'&uin=(.*?)&', self._url)
        self.f_uin = f_uin[0] if f_uin else ''
        
        pass_ticket_old = re.findall(r'&pass_ticket=(.*?)&', self._url)
        pass_ticket = re.subn('%', '%2525', pass_ticket_old[0])
        self.pass_ticket = pass_ticket[0]
        # print(self.start)
        # print(self.uin)
        # print(self.key)
        # print(self.f)
        # print(self.frommsgid)
        # print(self.count)
        # print(self.f_uin)
        # print(self.pass_ticket)
        # print(self.wxtoken)
        # print(self.x5)

        # print(self.start + '&uin=' + self.uin + '&key=' + self.key + '&f=' + self.f)
        full_url = self.start + '&uin=' + self.uin + '&key=' + self.key + '&f=' + self.f + '&frommsgid=' + str(self.frommsgid) + '&count=' + self.count + '&uin=' + self.f_uin + '&key=' + self.key + '&pass_ticket=' + self.pass_ticket + '&wxtoken=' + self.wxtoken + '&x5=' + self.x5
        # print(full_url)
        self.get_data(full_url)
        # full_url = 
        # pass_ticket_string = '&pass_ticket='
        # pass_ticket_operate = re.findall(r'' + pass_ticket_string + '(.*?)%', self._url)
        # pass_ticket_string = pass_ticket_string + pass_ticket_operate[0] + '%'
        # print(pass_ticket_string)
        # self.pass_ticket = self.pass_ticket + pass_ticket_operate[0] + '%2525'
        # print(pass_ticket_operate)
        # print(self.pass_ticket)
    
    def get_data(self, url):
        # request = urllib.request.Request(url, headers = self._headers)
        # response = self.opener.open(request)
        # print(response.read().decode('UTF-8'))
        # content = response.read().decode('UTF-8')
        # soup = bs4.BeautifulSoup(open("page2.json"), "lxml")
        data = open("page2.json", "r").read()
        msg_data = simplejson.loads(data)
        general_msg_list = msg_data.get('general_msg_list') if msg_data.get('errmsg') == 'ok' else ''
        general_msg_dict = simplejson.loads(general_msg_list).get('list')
        count = msg_data.get('count')
        if count > 9:
            self.flag = True
        print(general_msg_dict)
        
        # soup = bs4.BeautifulSoup(r.text,"html.parser")
        # print(r)




wechat = Wechat()
wechat.get_articles_from_first()