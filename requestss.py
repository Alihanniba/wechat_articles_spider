#_*_coding: utf-8 _*_
#__author__ = 'Alihanniba'

import requests

r = requests.get('https://www.alihanniba.com/')
print(type(r))
print(r.status_code)
print(r.encoding)
print(r.cookies)