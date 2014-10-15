# coding=utf-8
__author__ = 'BaiYa'

import urllib2

class HtmlDownload:
    def __init__(self, htmlUrl=None):
        self.url = htmlUrl
        pass

    def reader(self):
        return urllib2.urlopen(self.url).read()