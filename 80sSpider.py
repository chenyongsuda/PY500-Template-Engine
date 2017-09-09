# coding: utf-8
import requests
from bs4 import BeautifulSoup
from lxml import etree

import sys

reload(sys)
sys.setdefaultencoding('utf8')

web_base = 'http://www.80s.tw/'


class MediaBase:
    code = ""
    name = ""
    url = ""
    score = 0
    imgpath = ""

    type = ""
    area = ""
    lan = ""
    dir = ""
    start_data = ""
    update_date = ""
    time = ""
    dis = ""
    dn_list = {}

    def __init__(self):
        pass


def GetMovieListBaseInfos():
    MovieList = []
    i = 1
    page_obj = None
    before_ls = []
    while True:
        page_ls = []
        if i == 1:
            page_obj = requests.get('http://www.80s.tw/movie/list/-----p')
        else:
            page_obj = requests.get('http://www.80s.tw/movie/list/-----p%d' % i)
        soup = BeautifulSoup(page_obj.text, "html5lib")
        movie_ls = soup.select('ul.me1 > li')

        for li in movie_ls:
            itemsum_url = li.a['href']
            itemsum_name = li.a['title']
            itemsum_imgurl = li.a.img['_src']
            itemsum_imgsrc = li.a.img['src']
            itemsum_score = li.a.select_one('.poster_score').string if li.a.select_one('.poster_score') != None else ""

            item = li.select_one('h3 > a')
            item_url = item['href']
            item_name = item.string

            media = MediaBase()
            media.code = itemsum_url.split('/')[2]
            media.name = item_name.strip()
            media.url = itemsum_url.strip()
            media.score = itemsum_score.strip()
            media.imgpath = itemsum_imgurl.strip()
            page_ls.append(media)
        if len(page_ls) <= 0 or (len(before_ls) > 0 and (page_ls[0].code == before_ls[0].code)):
            break
        MovieList.extend(page_ls)
        before_ls = page_ls
        print i
        i += 1
    return MovieList


def GetMoiveItemDetails(media):
    page_obj = requests.get(web_base + media.url)
    html = etree.HTML(page_obj.text)
    media.type = html.xpath('//*[@id="minfo"]/div[2]/div[1]/span[1]/a/text()')
    media.area = html.xpath('//*[@id="minfo"]/div[2]/div[1]/span[2]/a/text()')
    media.lan = html.xpath('//*[@id="minfo"]/div[2]/div[1]/span[3]/a/text()')
    media.dir = html.xpath('//*[@id="minfo"]/div[2]/div[1]/span[4]/a/text()')
    media.start_data = html.xpath('//*[@id="minfo"]/div[2]/div[1]/span[5]/text()')
    media.update_date = html.xpath('//*[@id="minfo"]/div[2]/div[1]/span[7]/text()')
    media.time = html.xpath('//*[@id="minfo"]/div[2]/div[1]/span[6]/text()')
    media.dis = html.xpath('//*[@id="movie_content"]/text()[1]')


def GetMovieDownLoadList(media):
    types = ['bd-1', 'bt-1', 'hd-1', 'mp4-1']
    items = {}
    for type in types:
        page_obj = requests.get(('http://www.80s.tw/movie/%s/%s') % (media.code, type))
        soup = BeautifulSoup(page_obj.text, "html5lib")
        movie_info_linkdiv = soup.select('.dllist1 .dlurlelement')
        wapper = []
        for linkdiv in movie_info_linkdiv:
            item = [];
            item_url_xunlei = linkdiv.select_one('.dlbutton1 a')
            item_url_feitu = linkdiv.select_one('.dlbutton2 a')
            xunlei = (item_url_xunlei['href'] if (
                item_url_xunlei and item_url_xunlei.attrs and item_url_xunlei.attrs.has_key('href')) else '')

            feitu = item_url_feitu['src'] if (
                item_url_feitu and item_url_feitu.attrs and item_url_feitu.attrs.has_key('src')) else ''
            if len(xunlei) > 0:
                item.append(xunlei)
            if len(feitu) > 0:
                item.append(feitu)
            if len(xunlei) > 0 or len(feitu) > 0:
                wapper.append(item)
        if len(wapper) > 0:
            items[type] = wapper
    media.dn_list = items


def GetMoiveListDetails():
    list = GetMovieListBaseInfos()
    print len(list)
    for item in list:
        GetMoiveItemDetails(item)
        GetMovieDownLoadList(item)
        print item.code + "  " + item.name + " " + item.score
        print item.dn_list.keys()


GetMoiveListDetails()

# types = ['bd-1', 'bt-1', 'hd-1', 'mp4-1']
# items = {}
# for type in types:
#     page_obj = requests.get(('http://www.80s.tw/ju/21362/%s') % (type))
#     soup = BeautifulSoup(page_obj.text, "html5lib")
#     movie_info_linkdiv = soup.select('.dllist1 .dlurlelement')
#     wapper = []
#     for linkdiv in movie_info_linkdiv:
#         item = [];
#         item_url_xunlei = linkdiv.select_one('.dlbutton1 a')
#         item_url_feitu = linkdiv.select_one('.dlbutton2 a')
#         xunlei = (item_url_xunlei['href'] if (
#             item_url_xunlei and item_url_xunlei.attrs and item_url_xunlei.attrs.has_key('href')) else '')
#
#         feitu = item_url_feitu['src'] if (
#             item_url_feitu and item_url_feitu.attrs and item_url_feitu.attrs.has_key('src')) else ''
#         if len(xunlei) > 0:
#             item.append(xunlei)
#         if len(feitu) > 0:
#             item.append(feitu)
#         if len(xunlei) > 0 or len(feitu) > 0:
#             wapper.append(item)
#     items[type] = wapper
# print items

# # http://www.80s.tw/movie/20775/bd-1    TV
# # http://www.80s.tw/movie/20775/bt-1   1024
# # http://www.80s.tw/movie/676/hd-1 640
# # http://www.80s.tw/movie/676/mp4-1    480
# page_obj = requests.get('http://www.80s.tw/movie/20775/bd-1')
# soup = BeautifulSoup(page_obj.text, "html5lib")
# movie_info_linkdiv = soup.select('.dllist1 .dlurlelement')
# for linkdiv in movie_info_linkdiv:
#     item_url_xunlei = linkdiv.select_one('.dlbutton1 a')
#     item_url_feitu = linkdiv.select_one('.dlbutton2 a')
#     print '-------------------------------'
#     print (item_url_xunlei['href'] if (
#     item_url_xunlei and item_url_xunlei.attrs and item_url_xunlei.attrs.has_key('href')) else '')
#     print (
#     item_url_feitu['src'] if (item_url_feitu and item_url_feitu.attrs and item_url_feitu.attrs.has_key('src')) else '')
