# coding=utf-8
__author__ = 'BaiYa'

from DBStore import *
from HttpRequest import request
import re
import base64
import Logger

re_pics_url = "qTcms_S_m_murl_e=\"(\S*)\""

class PicController:

    def __init__(self, plot_id):
        self.session = session
        self.plot = self.session.query(Plot).filter(Plot.id==plot_id).first()

    def refreshPlot(self):
        if(not self.plot): return

        httpResponse = request(self.plot.link)
        if 200 != httpResponse.status:
            return
        result = httpResponse.data

        findAll = re.findall(re_pics_url, result.decode('gbk').encode('utf-8'))
        if (not len(findAll)):
            return
        picUrls = base64.decodestring(findAll[0])
        picList = picUrls.split('$qingtiandy$')

        Logger.info(str('pic list plot_id: %d' % self.plot.id))
        print(picList)

        for pic in self.plot.pic:
            self.session.delete(pic)

        for url in picList:
            page = picList.index(url) + 1
            pic = Pic(plot_id=self.plot.id, page=page, link=url)
            self.plot.pic.append(pic)
        self.session.commit()

if __name__ == '__main__':
    plotId = 1
    picController = PicController(plotId)
    picController.refreshPlot()
