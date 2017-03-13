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

class Wechat:
    def __init__(self, url=False):
        #获取随机IP
        # self._host = request_ip.RequestIP().getIP()
        self._url = url if url else 'https://mp.weixin.qq.com/mp/getmasssendmsg?__biz=MzI4MTA2OTA1Mg==&from=1&uin=MjA0NjcxNzUwMA%3D%3D&key=c6f43e46893b1d7168577e575e9e5c8aad63472dfc50c7a85c0b75f03e8906421832231046709cbd8f24df1be62c50cb2e91ef0fdcaf8d4db43f5afc8114dec7f4ee0ba59cff457fcdb9c27d787ee323&devicetype=iMac+MacBookPro12%2C1+OSX+OSX+10.12.3+build(16D32)&version=12010310&lang=zh_CN&nettype=WIFI&ascene=0&fontScale=100&pass_ticket=FTqCr1yuWBC9yttmCpq8Bvic%2Bb5n93XB9SGPNxzCouAupq1k4hf3OAl3feIrc%2BOc#wechat_webview_type=1'
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
        request = urllib.request.Request(self._url, headers = self._headers)
        response = self.opener.open(request)
        content = response.read().decode('UTF-8')
        # 保存cookie到cookie.txt中,  ### 其实不用
        self.cookie.save(ignore_discard=True, ignore_expires=True)  
        #以html解析格式打开
        soup = bs4.BeautifulSoup(content,"html.parser")
        #获取script节点
        script = soup.body.find_all("script")
        #数据在最后一个script节点中
        data = script[-1]
        #解析所需参数
        uin = re.findall(r'uin = "(\S+)"', str(data))
        key = re.findall(r'key = "(\S+)"', str(data))
        self.uin = uin[0] if uin else ''
        self.key = key[0] if key else ''
        msg_list = re.findall(r'msgList = {(.*?)};', str(data),re.S)
        msg_list_str = "{" + msg_list[0] + "}"
        #转为字典
        msg_list_dict = simplejson.loads(msg_list_str)
        app_msg_list = msg_list_dict.get("list")
        self.articles_list += app_msg_list
        
        self.frommsgid = app_msg_list[9].get('comm_msg_info').get('id') if len(app_msg_list) > 9 else self.frommsgid
        f_uin = re.findall(r'&uin=(.*?)&', self._url)
        self.f_uin = f_uin[0] if f_uin else self.f_uin
        
        pass_ticket_old = re.findall(r'&pass_ticket=(.*?)[&|#]', self._url)
        pass_ticket = re.subn('%', '%2525', pass_ticket_old[0])
        self.pass_ticket = pass_ticket[0]

        #拼装URL
        full_url = self.start + '&uin=' + self.uin + '&key=' + self.key + '&f=' + self.f + '&frommsgid=' + str(self.frommsgid) + '&count=' + self.count + '&uin=' + self.f_uin + '&key=' + self.key + '&pass_ticket=' + self.pass_ticket + '&wxtoken=' + self.wxtoken + '&x5=' + self.x5
        self.get_data(full_url)

    def get_data(self, url):
        request = urllib.request.Request(url, headers = self._headers)
        response = self.opener.open(request)
        content = response.read().decode('UTF-8')
        # content = open("page2.json", "r").read()
        msg_data = simplejson.loads(content)
        general_msg_list = msg_data.get('general_msg_list') if msg_data.get('errmsg') == 'ok' else ''
        general_msg_dict = simplejson.loads(general_msg_list).get('list')

        #拼接队列
        self.articles_list += general_msg_dict

        #weixin api 默认一次返回10条，小于10条则不进行下一次请求
        count = msg_data.get('count')
        self.flag = True if count > 9 else False
        
        if self.flag:
            #递归调用，仅frommsgid发生变化，微信下一页数据获取方式是拿当前页最后一条数据的ID作为参数请求URL
            self.frommsgid = general_msg_dict[9].get('comm_msg_info').get('id')
            full_url = self.start + '&uin=' + self.uin + '&key=' + self.key + '&f=' + self.f + '&frommsgid=' + str(self.frommsgid) + '&count=' + self.count + '&uin=' + self.f_uin + '&key=' + self.key + '&pass_ticket=' + self.pass_ticket + '&wxtoken=' + self.wxtoken + '&x5=' + self.x5
            self.get_data(full_url)
        else:
            splited_data = []

            for index, element in enumerate(self.articles_list):
                #app_msg_ext_info
                app_msg_ext_info = element.get('app_msg_ext_info')

                copyright_stat = app_msg_ext_info.get('copyright_stat')
                content_url = app_msg_ext_info.get('content_url')
                subtype = app_msg_ext_info.get('subtype')
                is_multi = app_msg_ext_info.get('is_multi')
                author = app_msg_ext_info.get('author')
                cover = app_msg_ext_info.get('cover')
                title = app_msg_ext_info.get('title')
                content = app_msg_ext_info.get('content')
                source_url = app_msg_ext_info.get('source_url')
                fileid = app_msg_ext_info.get('fileid')
                custom = 1 if author == 'Alihanniba' else 2
                
                #comm_msg_info
                comm_msg_info = element.get('comm_msg_info')

                wechat_id = comm_msg_info.get('id')
                status = comm_msg_info.get('status')
                wechat_type = comm_msg_info.get('type')
                datetime = comm_msg_info.get('datetime')
                fakeid = comm_msg_info.get('fakeid')

                #处理带有特殊字符字段
                digest = "GO TO BE A FULL STACK \n GO TO BE A ARCHITECT" if wechat_id == 1000000001 else app_msg_ext_info.get('digest')

                #组装数据，批量插入
                a_strip_data = (copyright_stat, content_url, subtype, is_multi, author, cover, title, digest, content, source_url, fileid, custom, wechat_id, status, wechat_type, datetime, fakeid )
                splited_data.append(a_strip_data)

                #连接数据库执行数据库操作
                db=pymysql.connect(host="localhost",user="alihanniba",charset="utf8",password="",db="alihanniba.com");  
                cursor=db.cursor()  

            #创建表，创建表之前应判断数据库中此表是否已存在，存在则删除
            sql="""CREATE TABLE IF NOT EXISTS `api_articles` ( 
                `id` int(11) NOT NULL AUTO_INCREMENT, 
                `copyright_stat` int(11) , 
                `content_url` text , 
                `subtype` int(11) , 
                `is_multi` int(11) , 
                `author` varchar(256) , 
                `cover` text , 
                `title` varchar(256) , 
                `digest` text , 
                `content` text , 
                `source_url` text , 
                `fileid` int(11) , 
                `custom` int(1) , 
                `wechat_id` int(11) , 
                `status` int(11) , 
                `wechat_type` int(11) , 
                `datetime` int(11) , 
                `fakeid` varchar(256) , 
                PRIMARY KEY (`id`) 
                ) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=0"""  
            
            cursor.execute(sql)  

            try:  
                # 执行sql语句  
                cursor.executemany('INSERT INTO api_articles (copyright_stat, content_url, subtype, is_multi, author, cover, title, digest, content, source_url, fileid, custom, wechat_id, status, wechat_type, datetime, fakeid) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',  splited_data)  
                # 提交到数据库执行  
                db.commit() 
                print('进入到插入步骤，请等待......') 
            except pymysql.InternalError as error: 
                code, message = error.args
                print(">>>>>>>>>>>>>", code, message) 
                # 如果发生错误则回滚 
                print('发生错误，插入失败') 
                db.rollback() 
            db.close()
            cursor.close()
            print('插入数据库完毕')

wechat = Wechat()
wechat.get_articles_from_first()