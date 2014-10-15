# coding=utf-8
__author__ = 'BaiYa'

import re
from bs4 import BeautifulSoup
from manga_db import *
from datetime import date, datetime

Zimu_Url = 'http://www.jide123.com/zimu/%s.html'
Base_Url = 'http://www.jide123.com'

def zimu_parse(html):
    re_manga_info_simple = "<dt><a href=\"(\S*)\" title=\"[^\"]*\">[^<]*</a></dt>"
    findAll = re.findall(re_manga_info_simple, html)
    mangas_link = []
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
        print(tag)
        plot_link = Base_Url + tag['href']
        plot_index = plot_count - tag_a.index(tag)
        plot_title = tag.contents[0]
        plot = Plot(link=plot_link, title=plot_title, index=plot_index)
        plots.append(plot)
    return plots


def manga_parse(html, source):
    soup = BeautifulSoup(html, from_encoding='gbk')
    # print(soup.prettify())
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
    # print(title)
    # print(author)
    # print(cover)
    # print(intro)
    # print(search)
    # print(added_time)
    # print(up_time)
    return Manga(
        added_at=added_time,
        update_at=up_time,
        name=title,
        author=author,
        introduction=intro,
        poster=cover,
        source=source,
        plot=plot)

from request import request
from html_parse.html_parse import *
import pic_controller
from pic_controller import *
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
    # low = 0
    # high = len(plots) - 1
    # while(low <= high):
    #     mid = (low + high) / 2
    #     midIndex = plots[mid].index
    #     if(midIndex < index):
    #         low = mid + 1
    #     elif(midIndex > index):
    #         high = mid - 1
    #     else:
    #         return plots[mid]
    # return None
    pass

if __name__ == '__main__':
    for index in initials:
        if (index != 'a'): break

        result = request(str(Zimu_Url % index)).read()
        mangas_link = zimu_parse(result.decode('gbk').encode('utf-8'))

        print(len(mangas_link))

        init_db()
        Session = sessionmaker(bind=engine)
        session = Session()

        for manga_link in mangas_link:
            # if(0 != mangas_link.index(manga_link)):
            #     continue
            print(manga_link)
            result = request(manga_link).read()
            manga = manga_parse(result, manga_link)
            query_result = session.query(Manga).filter(Manga.name==manga.name).first()
            if(query_result):
                assign(manga.name, query_result.name)
                assign(manga.added_at, query_result.added_at)
                assign(manga.update_at, query_result.update_at)
                assign(manga.author, query_result.author)
                assign(manga.source, query_result.source)
                assign(manga.poster, query_result.poster)
                assign(manga.introduction, query_result.introduction)
                # 更新剧情信息

                ''' 已知元素X有index属性。数组A中有i个元素，数组B中有j个元素，遍历数组A，并找到B中含有相同index属性的元素，更新或添加到A中？
                '''
                # 根据plot.index排序
                # query_result.plot.sort(key=lambda plot: plot.index)
                for item in manga.plot:
                    print(item.index)
                    query_plot = queryPlotWithIndex(item.index, query_result.plot)
                    print(query_plot)
                    if (query_plot):
                        assign(item.title, query_plot.title)
                        assign(item.link, query_plot.link)
                    else:
                        plot_new = Plot(manga_id=query_result.id, link=item.link, title=item.title, index=item.index)
                        query_result.plot.append(plot_new)
            else:
                session.add(manga)
            session.commit()

            query_result = session.query(Manga).filter(Manga.name==manga.name).first()
            print(query_result.plot)
            plots = query_result.plot
            for plot in plots:
                pic_controller = PicController(plot.id)
                pic_controller.refreshPlot()
        pass
