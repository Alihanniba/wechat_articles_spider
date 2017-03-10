#_*_coding: utf-8 _*_
#__author__ = 'Alihanniba'

import requests
from bs4 import BeautifulSoup
import re

html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
    <title>TO BE A FULL STACK, TO BE A ARCHITECT</title>
    <meta name="keywords" content="阿里汉尼拔,汉尼拔,移动开发,Android开发,iOS开发,前端开发,后端开发,产品设计,资源下载,React.js,vue.js,node.js,编程,程序员,开发者,设计师,产品经理,Hacker News,ECMAScript,开源,Github">
    <meta name="description" content="alihanniba,阿里汉尼拔个人网站,博客日志系统,记录个人代码与成长历程,花一个无所谓的年纪去浪荡">
    <meta name="csrf-token" content=""/>
    <meta name="author" content="alihanniba">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black">
    <link rel="apple-touch-icon" sizes="57x57" href="">
    <link rel="apple-touch-icon" sizes="60x60" href="">
    <link rel="apple-touch-icon" sizes="72x72" href="">
    <link rel="apple-touch-icon" sizes="76x76" href="">
    <link rel="apple-touch-icon" sizes="114x114" href="">
    <link rel="apple-touch-icon" sizes="120x120" href="">
    <link rel="apple-touch-icon" sizes="144x144" href="">
    <link rel="apple-touch-icon" sizes="152x152" href="">
    <link rel="apple-touch-icon" sizes="180x180" href="">
    <link rel="icon" type="image/png" sizes="192x192"  href="">
    <link rel="icon" type="image/png" sizes="32x32" href="">
    <link rel="icon" type="image/png" sizes="96x96" href="">
    <link rel="icon" type="image/png" sizes="16x16" href="">
    <link rel="manifest" href="manifest.json">
    <meta name="msapplication-TileColor" content="#ffffff">
    <meta name="msapplication-TileImage" content="">
    <meta name="theme-color" content="#ffffff">
    <style>
        #root {
            height: 100%;
            width: 100%;
        }
    </style>
<link rel="shortcut icon" href="/mylogo.jpg"></head>
<body>
<div id="root">
</div>
<script src="//cdn.bootcss.com/react/15.4.1/react.min.js"></script>
<script src="//cdn.bootcss.com/react/15.4.1/react-dom.min.js"></script>
<script src="//cdn.bootcss.com/react/15.4.1/react-dom-server.min.js"></script>
<script src="//cdn.bootcss.com/react-router/2.8.1/ReactRouter.min.js"></script>
<script src="//cdn.bootcss.com/redux/3.5.2/redux.min.js"></script>
<script src="//cdn.bootcss.com/react-redux/4.4.5/react-redux.min.js"></script>
<script src="//cdn.bootcss.com/react-router-redux/4.0.5/ReactRouterRedux.min.js"></script>
<script type="text/javascript" src="/acb8ffed.bundle.js"></script></body>
</html>
"""

soup = BeautifulSoup(html)

# print(soup.prettify())
print(soup.div)
print(soup.script)
print('=============')

print(soup.title)
print(type(soup.title))
print('=============')

print(soup.title.string)
print(type(soup.title.string))
print('=============')

print(soup.head)
print(soup.head.contents[0])
print('=============')

for child in soup.descendants:
    print(child)
print('=============')

print(soup.find_all('div'))
print('=============')

for tag in soup.find_all(re.compile('^div')):
    print(tag.name)
print('=============')

for tag in soup.find_all(True):
    print(tag.name)

print('=============')

def has_id(tag):
    return tag.has_attr('id')
soup.find_all(has_id)
print('=============')


print(soup.find_all(id='root'))
print('=============')

print(soup.select('title'))
print(soup.select('head'))

