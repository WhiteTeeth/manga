# coding=utf-8
__author__ = 'BaiYa'

from HttpRequest import HttpRequest
from html_parse import Parse

class Scrapy(object):

    def __init__(self, request, parse):
        self.request = request
        self.parse = parse
        pass

    def scrapy(self):
        # if isinstance(self.request, HttpRequest) and isinstance(self.parse, Parse):
        self.request.request()
        if 304 == self.request.status:
            self.parse.parse(self.request, False)
        elif 200 == self.request.status:
            self.parse.parse(self.request, True)
        else:
            self.parse.parse(self.request, True)
    pass
