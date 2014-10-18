# coding=utf-8
__author__ = 'BaiYa'

import re
from bs4 import BeautifulSoup
from DBStore import *
from datetime import date, datetime

Zimu_Url = 'http://www.jide123.com/zimu/%s.html'
Base_Url = 'http://www.jide123.com'

def zimu_parse(html):
    if not html:
        return []
    mangas_link = []
    re_manga_info_simple = "<dt><a href=\"(\S*)\" title=\"[^\"]*\">[^<]*</a></dt>"
    findAll = re.findall(re_manga_info_simple, html)
    for item in findAll:
        link = Base_Url + item
        mangas_link.append(link)
    return mangas_link

def plot_parse(soup, source):
    plot_html = soup.find('div', id='play_0')
    tag_a = plot_html.find_all('a')
    plots = []
    plot_count = len(tag_a)
    for tag in tag_a:
        plot_link = Base_Url + tag['href']
        plot_index = plot_count - tag_a.index(tag)
        plot_title = tag.contents[0]
        plot = Plot(link=plot_link, title=plot_title, index=plot_index)
        plots.append(plot)
    return plots

def manga_parse(html, source):
    if not html:
        Logger.info('html is empty!')
        return None
    soup = BeautifulSoup(html, from_encoding='gbk')
    # Logger.debug(soup.prettify())
    intro = soup.find(id='intro_l')
    title = intro.find('h1').string.decode('utf-8').encode('utf-8')
    search = soup.find_all('p', attrs={'class':'w260'})
    up_time = search[0].find('span').string
    tmp = search[1].contents
    if(len(tmp) > 1):
        author = tmp[1]
    else:
        author = ''
    added_time = search[2].contents[1]
    cover = soup.find('div', attrs={'class':'info_cover'}).p.img['src']
    intro = soup.find('div', id='intro1').p.string
    if(intro):
        intro = intro.strip()
    up_time = datetime.strptime(up_time, '%Y-%m-%d').date()
    added_time = datetime.strptime(added_time, '%Y-%m-%d').date()
    plot = plot_parse(soup, source)
    return Manga(
        added_at=added_time,
        update_at=up_time,
        name=title,
        author=author,
        introduction=intro,
        poster=cover,
        source=source,
        plot=plot)

def manga_refresh(manga):
    query = session.query(Manga).filter(Manga.name==manga.name).first()
    if(query):
        assign(manga.name, query.name)
        assign(manga.added_at, query.added_at)
        assign(manga.update_at, query.update_at)
        assign(manga.author, query.author)
        assign(manga.source, query.source)
        assign(manga.poster, query.poster)
        assign(manga.introduction, query.introduction)

        # 更新剧情信息
        for item in manga.plot:
            query_plot = queryPlotWithIndex(item.index, query.plot)
            if (query_plot):
                assign(item.title, query_plot.title)
                assign(item.link, query_plot.link)
            else:
                plot_new = Plot(manga_id=query.id, link=item.link, title=item.title, index=item.index)
                query.plot.append(plot_new)
    else:
        session.add(manga)
    session.flush()
    pass

def pic_parse(html, source):
    import base64
    re_pics_url = "qTcms_S_m_murl_e=\"(\S*)\""
    findAll = re.findall(re_pics_url, html.decode('gbk').encode('utf-8'))
    if (not len(findAll)):
        return
    picUrls = base64.decodestring(findAll[0])
    picList = picUrls.split('$qingtiandy$')
    return picList


from assign import assign

initials = ['a', 'b', 'c', 'd', 'e', 'f', 'g',
         'h', 'i', 'j', 'k', 'l', 'm', 'n',
         'o', 'p', 'q', 'r', 's', 't',
         'u', 'v', 'w', 'x', 'y', 'z']

def queryPlotWithIndex(index, plots):
    '''
    查询plots中相同index的plot, 没有返回None
    '''
    for plot in plots:
        if(plot.index == index):
            return plot
    return None
    pass

from HttpRequest import request
import Logger

if __name__  == '__main__':
    init_db()
    for index in initials:
        if (index != 'u'): continue

        url = str(Zimu_Url % index)
        result = request(url, ignoreCache=True)
        if 200 != result.status:
            continue
        httpResponse = result.data

        mangas_link = zimu_parse(httpResponse.decode('gbk').encode('utf-8'))

        Logger.info(str('manga --%s-- count:%d' % (index, len(mangas_link))))

        for manga_link in mangas_link:
            if(0 != mangas_link.index(manga_link)):
                continue

            result = request(manga_link, ignoreCache=True)
            if result.status != 200:
                continue

            httpResponse = result.data
            #更新漫画剧情信息
            manga = manga_parse(httpResponse, manga_link)
            manga_refresh(manga)

            #更新单集漫画信息
            query = session.query(Manga).filter(Manga.name==manga.name).first()
            plots = query.plot
            for plot in plots:
                result = request(plot.link, ignoreCache=True)
                if 200 != result.status:
                    continue
                httpResponse = result.data
                picList = pic_parse(httpResponse, plot.link)

                for pic in plot.pic:
                    session.delete(pic)

                for url in picList:
                    page = picList.index(url) + 1
                    pic = Pic(plot_id=plot.id, page=page, link=url)
                    plot.pic.append(pic)
                session.flush()
        session.commit()
        session.close()
        pass
