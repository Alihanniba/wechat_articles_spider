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
    def __init__(self, url=False):
        #获取随机IP
        self._host = request_ip.RequestIP().getIP()
        # self._url = 'https://mp.weixin.qq.com/mp/getmasssendmsg?__biz=MzI4MTA2OTA1Mg==&from=1&uin=MjA0NjcxNzUwMA%3D%3D&key=a9d7e7f2647cda56c09277a9e1a47fef133d1a25b4cfd8eeead76f2aed61c6f5355e67e48837ab9a3dad64409f91ed579ef27c1997432f18a6784cdbfbbb867e8e6586c247e49dd4865212ca4d7271e9&devicetype=iMac+MacBookPro12%2C1+OSX+OSX+10.12.3+build(16D32)&version=12010310&lang=zh_CN&nettype=WIFI&ascene=0&fontScale=100&pass_ticket=9VNc%2BuPHO2Yfrgz2GS%2BZ5LA28LMVeV9fUaLHjtjIJZnP4deavqs3KHmdZ%2F%2Bax1Oo#wechat_webview_type=1'
        
        self._url = url if url else 'https://mp.weixin.qq.com/mp/getmasssendmsg?__biz=MzI4MTA2OTA1Mg==&from=1&uin=MjA0NjcxNzUwMA%3D%3D&key=0be43264c9a5f2c381bd53c1176598cbde0da45f08902746476fe12be756abcee4a8fab9ba5ac8edd800897f7ccebcf21dcc903df3b270b2b3f01e9ecbceada295b9e04fc9c42865871724da2fdd3f9e&devicetype=iMac+MacBookPro12%2C1+OSX+OSX+10.12.3+build(16D32)&version=12010310&lang=zh_CN&nettype=WIFI&ascene=0&fontScale=100&pass_ticket=FTqCr1yuWBC9yttmCpq8Bvic%2Bb5n93XB9SGPNxzCouAupq1k4hf3OAl3feIrc%2BOc#wechat_webview_type=1'
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

        #集中返回的所有数据以便进一步分析存库
        self.articles_list = []   
    
    def get_articles_from_first(self):
        # request = urllib.request.Request(self._url, headers = self._headers)
        # response = self.opener.open(request)
        # content = response.read().decode('UTF-8')
        # self.cookie.save(ignore_discard=True, ignore_expires=True)  # 保存cookie到cookie.txt中
        # soup = bs4.BeautifulSoup(content,"html.parser")
        # # soup = bs4.BeautifulSoup(open("page1.html"), "lxml")
        # # minMsgId = soup.script.find_all("script", limit=40)
        # # print(soup.prettify()) # 格式化输出
        # script = soup.body.find_all("script")
        # data = script[-1]
        # uin = re.findall(r'uin = "(\S+)"', str(data))
        # key = re.findall(r'key = "(\S+)"', str(data))
        # self.uin = uin[0] if uin else ''
        # self.key = key[0] if key else ''
        # msg_list = re.findall(r'msgList = {(.*?)};', str(data),re.S)
        # msg_list_str = "{" + msg_list[0] + "}"
        # #转为字典
        # msg_list_dict = simplejson.loads(msg_list_str)
        # app_msg_list = msg_list_dict.get("list")
        # self.articles_list += app_msg_list
        # self.frommsgid = app_msg_list[9].get('comm_msg_info').get('id') if len(app_msg_list) > 9 else self.frommsgid
        # f_uin = re.findall(r'&uin=(.*?)&', self._url)
        # self.f_uin = f_uin[0] if f_uin else self.f_uin
        
        # pass_ticket_old = re.findall(r'&pass_ticket=(.*?)[&|#]', self._url)
        # pass_ticket = re.subn('%', '%2525', pass_ticket_old[0])
        # self.pass_ticket = pass_ticket[0]
        # # print(self.start)
        # # print(self.uin)
        # # print(self.key)
        # # print(self.f)
        # # print(self.frommsgid)
        # # print(self.count)
        # # print(self.f_uin)
        # # print(self.pass_ticket)
        # # print(self.wxtoken)
        # # print(self.x5)

        full_url = self.start + '&uin=' + self.uin + '&key=' + self.key + '&f=' + self.f + '&frommsgid=' + str(self.frommsgid) + '&count=' + self.count + '&uin=' + self.f_uin + '&key=' + self.key + '&pass_ticket=' + self.pass_ticket + '&wxtoken=' + self.wxtoken + '&x5=' + self.x5
        self.get_data(full_url)

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
        # content = response.read().decode('UTF-8')
        # # content = open("page2.json", "r").read()
        # msg_data = simplejson.loads(content)
        # general_msg_list = msg_data.get('general_msg_list') if msg_data.get('errmsg') == 'ok' else ''
        # general_msg_dict = simplejson.loads(general_msg_list).get('list')

        # #拼接队列
        # self.articles_list += general_msg_dict

        # #weixin api 默认一次返回10条，小于10条则不进行下一次请求
        # count = msg_data.get('count')
        # self.flag = True if count > 9 else False
        
        self.flag = False

        if self.flag:
            self.frommsgid = general_msg_dict[9].get('comm_msg_info').get('id')
            full_url = self.start + '&uin=' + self.uin + '&key=' + self.key + '&f=' + self.f + '&frommsgid=' + str(self.frommsgid) + '&count=' + self.count + '&uin=' + self.f_uin + '&key=' + self.key + '&pass_ticket=' + self.pass_ticket + '&wxtoken=' + self.wxtoken + '&x5=' + self.x5
            self.get_data(full_url)
        else:
            
            content = open("all_articles.json", "r").read()
            
            print(content)
            
        # soup = bs4.BeautifulSoup(r.text,"html.parser")
        # print(r)




wechat = Wechat()
wechat.get_articles_from_first()