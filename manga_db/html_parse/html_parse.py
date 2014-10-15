# coding=utf-8
__author__ = 'BaiYa'

import re
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

class HtmlParse:

    re_manga_info_simple = "<dt><a href=\"(\S*)\" title=\"(\S*)\">(\S*)</a></dt>"

    def __init__(self, html=None):
        self.html = html
        print(html)
        foundAll = re.findall(HtmlParse.re_manga_info_simple, html)
        print(foundAll)
        # only_div_tag = SoupStrainer('dt')
        # self.soup = BeautifulSoup(html, 'html.parser', parse_only=only_div_tag)
        # print(self.soup)
        # self.mangas = self.__getMangas_()

    def __getMangas_(self):
        mangas_html = self.soup.find_all('div', id='dmList')[0]
        mangas = []
        # print(len(mangas_html.find_all('li')))
        # for manga_html in mangas_html.find_all('li'):
        #     mangas.append(self.__getManga_(manga_html))
        #     pass
        # print(mangas)
        # return mangas

    def __getManga_(self, html):

        pass

    pass