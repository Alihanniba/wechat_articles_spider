from random import choice
import requests
from bs4 import BeautifulSoup
import bs4
import re

class RequestIP:
    def __init__(self):
        self.url = 'http://www.xicidaili.com/nn'
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "Referer":"http://www.xicidaili.com/",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
        }
    
    def getIP(self):
        r = requests.get(self.url, headers = self.headers)
        soup = bs4.BeautifulSoup(r.text,"html.parser")
        td_data = soup.table.find_all("td", limit=40)
        ip_compile = re.compile(r"<td>(\d+\.\d+\.\d+\.\d+)</td>")
        port_compile = re.compile(r"<td>(\d+)</td>")
        ip = re.findall(ip_compile, str(td_data))
        port = re.findall(port_compile, str(td_data))
        ips = [":".join(i) for i in zip(ip,port)]
        return choice(ips)
q = RequestIP()
q.getIP()