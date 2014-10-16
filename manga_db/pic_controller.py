# coding=utf-8
__author__ = 'BaiYa'

from DBStore import *
# from HttpRequest import request
from HttpRequest import HttpRequest
from bs4 import BeautifulSoup
from assign import assign
import re
import base64

re_pics_url = "qTcms_S_m_murl_e=\"(\S*)\""

class PicController:

    def __init__(self, plot_id):
        init_db()
        Session = sessionmaker(bind=engine)
        self.session = Session()
        query_result = self.session.query(Plot).filter(Plot.id==plot_id).first()
        if(query_result):
            self.plot = query_result

    def refreshPlot(self):
        if(not self.plot): return
        link = self.plot.link

        httpRequest = HttpRequest(url=link)
        httpRequest.request()

        if httpRequest.status == 304:
            return
        elif httpRequest.status != 200:
            print('httpRequest header:', httpRequest.header)
            return
        result = httpRequest.data
        # result = request(link).read()
        findAll = re.findall(re_pics_url, result.decode('gbk').encode('utf-8'))
        if (not len(findAll)):
            return
        picUrls = base64.decodestring(findAll[0])
        picList = picUrls.split('$qingtiandy$')

        for pic in self.plot.pic:
            self.session.delete(pic)

        for url in picList:
            page = picList.index(url) + 1
            pic = Pic(plot_id=self.plot.id, page=page, link=url, source=self.plot.link)
            self.plot.pic.append(pic)
        self.session.commit()

    def __queryPicWith(self, page, pics):
        '''
        查询pics中相同page的pic, 没有返回None
        :param index:
        :param pics: 排序后pic列表，根据page从小往大排序
        :return:
        '''
        for pic in pics:
            if (pic.page == page):
                return pic

        # low = 0
        # high = len(pics) - 1
        # while(low <= high):
        #     mid = (low + high) / 2
        #     midIndex = pics[mid].page
        #     if(midIndex < page):
        #         low = mid + 1
        #     elif(midIndex > page):
        #         high = mid - 1
        #     else:
        #         return pics[mid]
        return None
        pass