# coding=utf-8
# 网络爬虫
__author__ = 'BaiYa'

from html_download import HtmlDownload

url = 'http://www.ishuhui.com/'
request = HtmlDownload(url)
response = request.reader()

print response

