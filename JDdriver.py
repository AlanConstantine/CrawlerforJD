# -*- coding: utf-8 -*-
# @Date  : 2017-10-05 16:25:48
# @Author: Alan Lau (rlalan@outlook.com)

import json
import time
import random
import requests
import collections
from JD_model import JDWires
from bs4 import BeautifulSoup
from pprint import pprint as p
from datetime import datetime as dt
from selenium import webdriver as wb
# from JD_model import Wires


class getCommentsJson:

    def __init__(self, commdict, page, goodsurl, driver):
        self.commdict = commdict
        self.page = page
        self.goodsurl = goodsurl
        self.current_url = str(driver.current_url)
        self.pid = (((self.current_url.split('.html'))[0])).split('/')[-1]
        self.url = "https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv3168&productId=" + \
            str(self.pid) + "&score=0&sortType=5&page=" + \
            str(self.page) + "&pageSize=10&isShadowSku=0&rid=0&fold=1"

    def buildHeader(self):
        headers = {
            "(Request-Line)": "GET /comment/productPageComments.action?callback=fetchJSON_comment98vv3168&productId=" + str(self.pid) + "&score=0&sortType=5&page=" + str(self.page) + "&pageSize=10&isShadowSku=0&rid=0&fold=1 HTTP/1.1",
            "Host": "club.jd.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0",
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": self.goodsurl,
            "Cookie": "__jda=122270672.90581397.1484812909.1507199291.1507200178.16; TrackID=1vWOcAGaoGu3DP1Y7-FQ-aCBcOxVsEQBJDNyI1WZDB8vYL7V9MwpguOf_bQmszVembrI2cYTNRKyDyuzKYeJMdpyvbaikfx0WqoYXnZCUOSY; pinId=wRFvsaVw07yHV9PQRreBdg; ipLoc-djd=1-72-2799-0; __jdv=122270672|baidu|-|organic|not set|1507200178039; __jdu=90581397; __jdc=122270672; mt_xid=V2_52007VwsTVlRYUFIZeU1cBDVQRgVURAYIGRwFWQA3Cw5aXw0GRkgeEFkDZAERAlsKVmocSBlaGWcCDlNZSVJdFE0fVwRmMxBiXWhbXh5JEFoFZwsRV1VbW1weSx1VNWcGFFU%3D; 3AB9D23F7A4B3C9B=GODTY6RVTUCN2KAXZHYKEUZSO7OJVOEDBIT2IMT6HS6LYVP4RR2YH7VGTMODAKIJUF6XICVDXY7Q2L7CNNCWIJJ7MM",
            "Connection": "keep-alive"
        }
        data = {
            "callback": "fetchJSON_comment98vv3168",
            "productId": self.pid,
            "score": "0",
            "sortType": "5",
            "page": self.page,
            "pageSize": "10",
            "isShadowSku": "0",
            "rid": "0",
            "fold": "1"
        }
        return headers, data

    def requestComments(self):
        headers, data = self.buildHeader()
        r = requests.post(url=self.url, headers=headers,  data=data)
        rj = (str(r.text).replace('fetchJSON_comment98vv3168(', ''))[:-2]
        rjdict = json.loads(rj)
        return rjdict

    def parserJson(self):
        rjdict = self.requestComments()
        json_comments = rjdict['comments']
        for com in json_comments:
            self.commdict[com['nickname']] = com['content']
        return self.commdict


# def scoll2end(driver):
#     pt = 0.5
#     last_height = driver.execute_script("return document.body.scrollHeight")
#     while True:
#         driver.execute_script(
#             "window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(pt)
#         new_height = driver.execute_script("return document.body.scrollHeight")
#         if new_height == last_height:
#             break
#         last_height = new_height


# def get_echcom(commdict, soup):
#     get_comments_div = soup.find(
#         'div', class_='J-comments-list comments-list ETab')
#     get_comms_num = get_comments_div.find('div', class_='tab-con')
#     get_allcomm = get_comms_num.find_all('div', class_='comment-item')
#     for com in get_allcomm:
#         get_user = (com.find('div', class_='user-info').get_text()).strip()
#         get_com_content = (
#             com.find('p', class_='comment-con').get_text()).strip()
#         commdict[get_user] = get_com_content
#     return commdict


def get_comments(comNum, url, driver, soup):
    pass
    commdict = {}

    st = 0.5
    et = 2

    comNumWoPlus = comNum.replace('+', '')
    if '万' in comNumWoPlus:
        comNumWoPlus = comNumWoPlus.replace('万', '')
        comNumWoPlus = int(comNumWoPlus * 10000)
    else:
        comNumWoPlus = int(comNumWoPlus)

    if comNumWoPlus < 10:

        commdict = getCommentsJson(
            commdict, 0, url, driver).parserJson()
        print('Total:%s, get comments from page:%s...' % (comNum, str(1)))
        return commdict
    elif comNum == '10+':
        commdict = getCommentsJson(
            commdict, 0, url, driver).parserJson()
        tp = random.uniform(st, et)
        print('Total:%s, get comments from page:%s, sleep:%ss...' %
              (comNum, str(1), str(round(tp, 2))))
        time.sleep(tp)
        commdict = getCommentsJson(
            commdict, 1, url, driver).parserJson()
        print('Total:%s, get comments from page:%s...' % (comNum, str(2)))
        return commdict
    elif comNumWoPlus < 100 and comNumWoPlus > 10:
        page_num = int(comNumWoPlus // 10) + 1
        for page in range(0, page_num):
            commdict = getCommentsJson(
                commdict, page, url, driver).parserJson()
            tp = random.uniform(st, et)
            print('Total:%s, get comments from page:%s, sleep:%ss...' %
                  (comNum, str(page + 1), str(round(tp, 2))))
            time.sleep(tp)
        return commdict
    else:
        for page in range(0, 10):
            commdict = getCommentsJson(
                commdict, page, url, driver).parserJson()
            tp = random.uniform(st, et)
            print('Total:%s, get comments from page:%s, sleep:%ss...' %
                  (comNum, str(page + 1), str(round(tp, 2))))
            time.sleep(tp)
        return commdict


def parser(get_detail, comNum, url, driver, soup):
    pass
    # get_detail = {}

    get_intro_ul = soup.find('ul', class_='parameter2 p-parameter-list')
    get_intro_li = get_intro_ul.find_all('li')
    intro = collections.OrderedDict()
    for li in get_intro_li:
        in_split = (li.get_text()).split('：')
        intro[in_split[0]] = in_split[-1]
    get_detail['introduction'] = str(dict(intro))

    main_framk = collections.OrderedDict()
    get_div_Ptable = soup.find('div', class_='Ptable')
    # item-detail
    # print(type(get_div_Ptable))
    if str(type(get_div_Ptable)) == "<class 'NoneType'>":
        get_div_detail = soup.find('div', class_='item-detail')
        main_framk['规格与包装'] = get_div_detail.get_text()
    else:
        get_div_Ptable_item = get_div_Ptable.find_all(
            'div', class_='Ptable-item')
        for div in get_div_Ptable_item:
            get_main = (div.find('h3')).get_text()
            dtls = []
            dts = div.find_all('dt')
            for dt in dts:
                dtls.append(dt.get_text())

            ddls = []
            dds = div.find_all('dd')
            for dd in dds:
                ddls.append(dd.get_text())
            d = collections.OrderedDict()
            if len(dd) == len(dt):
                assert 'Wronging!!!!!'
            for i in range(len(ddls)):
                d[dtls[i]] = ddls[i]
            main_framk[get_main] = dict(d)
    get_pl = soup.find('div', class_='package-list')
    if str(type(get_pl)) != "<class 'NoneType'>":
        h3 = get_pl.find('h3').get_text()
        p = get_pl.find('p').get_text()
        main_framk[h3] = p
    get_detail['specification'] = str(dict(main_framk))

    get_server_div = soup.find('div', class_='serve-agree-bd')
    dtls = []
    dts = get_server_div.find_all('dt')
    for dt in dts:
        dtls.append(str(dt.get_text()).strip())

    ddls = []
    dds = get_server_div.find_all('dd')
    for dd in dds:
        ddls.append(str(dd.get_text()).strip().replace(' ', ''))
    if len(dd) == len(dt):
        assert 'Wronging!!!!!'
    d = collections.OrderedDict()
    for i in range(len(ddls)):
        d[dtls[i]] = ddls[i]
    get_detail['aftersale'] = str(dict(d))

    if comNum == '0':
        get_detail['comments'] = 'no comment'
    else:
        commresulr = get_comments(comNum, url, driver, soup)
        get_detail['comments'] = str(commresulr)

    return get_detail


def jdriver(result, driver, url, comNum):
    # driver = wb.Ie()
    print(url)
    driver.get(url)
    driver.set_page_load_timeout(100)
    driver.set_window_size(0, 0)
    pagecontent = driver.page_source
    soup = BeautifulSoup(pagecontent, "html.parser")
    result = parser(result, comNum, url, driver, soup)

    driver.close()
    # driver.quit()
    return result


# def main():
#     data = Wires.select()
#     for datum in data:
#         driver = wb.Ie()
#         try:
#             print('Now getting id:%s...' % (datum.id))
#             result = jdriver(driver, datum.url, datum.commentnum)
#             result['id'] = datum.id
#             result['url'] = datum.url
#             result['title'] = datum.title
#             # p(result)
#             Wiresdetails.create(**result)
#             time.sleep(5)
#         except Exception as e:
#             print(e)
#             driver.close()
#             with open(r'errorlist.txt', 'a', encoding='utf8') as f:
#                 f.write(str(datum.id) + '\t' + str(e) + '\n')
#             pass
    # raise e

def detailCrawler(page, result):
    driver = wb.Ie()
    try:
        print('Now getting page:%s, id:%s...' % (page, result['id']))
        result = jdriver(result, driver, result['url'], result['comm_num'])
        JDWires.create(**result)
        time.sleep(5)
    except Exception as e:
        print(e)
        driver.close()
        with open(r'errorlist.txt', 'a', encoding='utf8') as f:
            f.write(str(result['id']) + '\t' +
                    'detail error' + '\t' + str(e) + '\n')
        pass


if __name__ == '__main__':
    ts = dt.now()
    main()
    te = dt.now()
    tdif = te - ts
    print('[%s]' % tdif)
