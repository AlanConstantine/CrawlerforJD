# -*- coding: utf-8 -*-
# @Date  : 2017-10-06 13:06:03
# @Author: Alan Lau (rlalan@outlook.com)

import requests
from bs4 import BeautifulSoup
from pprint import pprint as p
from reader import writetxt as wt
from JDdriver import detailCrawler
from datetime import datetime as dt

id = 0


def buildheader(page):
    page = 2 * page - 1
    url = 'https://search.jd.com/Search?keyword=%E7%94%B5%E7%BC%86%E7%BA%BF&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E7%94%B5%E7%BC%86%E7%BA%BF&page=' + \
        str(page) + '&s=58&click=0'
    headers = {
        "(Request-Line)": "GET /Search?keyword=%E7%94%B5%E7%BC%86%E7%BA%BF&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E7%94%B5%E7%BC%86%E7%BA%BF&page=" + str(page) + "&s=58&click=0 HTTP/1.1",
        "Host": "search.jd.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "Cookie": "__jda=122270672.90581397.1484812909.1507258086.1507266465.23; pg=true; TrackID=1vWOcAGaoGu3DP1Y7-FQ-aCBcOxVsEQBJDNyI1WZDB8vYL7V9MwpguOf_bQmszVembrI2cYTNRKyDyuzKYeJMdpyvbaikfx0WqoYXnZCUOSY; pinId=wRFvsaVw07yHV9PQRreBdg; xtest=8484.cf6b6759; ipLoc-djd=1-72-2799-0; __jdv=122270672|baidu|-|organic|not set|1507200178039; qrsc=3; __jdu=90581397; mt_xid=V2_52007VwsTVlRYUFIZeU5YBWQCGwFURAcISxoFWVU3AQ4BVF0GRh0eTQwDMldFUQhcVWocSBlaGWcCDlNaSVNdFEsYVwdhMxBiXWhbXh5JEFoFZwsRV1VbW1weSx1VNWcGFFU%3D; __jdb=122270672.2.90581397|23.1507266465; __jdc=122270672; rkv=V0200; 3AB9D23F7A4B3C9B=GODTY6RVTUCN2KAXZHYKEUZSO7OJVOEDBIT2IMT6HS6LYVP4RR2YH7VGTMODAKIJUF6XICVDXY7Q2L7CNNCWIJJ7MM"
    }
    data = {
        "keyword": "电缆线",
        "enc": "utf-8",
        "qrst": "1",
        "rt": "1",
        "stop": "1",
        "vt": "2",
        "wq": "电缆线",
        "page": str(page),
        "s": "58",
        "click": "0"
    }
    return url, headers, data


def reqweb(page):
    try:
        url, headers, data = buildheader(page)
        r = requests.get(url=url, headers=headers, data=data)
        s = BeautifulSoup(r.content, 'html.parser')
        getgoods = s.find_all('li', class_='gl-item')
        for g in getgoods:
            global id
            get_detail = {}
            get_price_div = g.find('div', class_='p-price')
            get_detail['price'] = float(get_price_div.find('i').string)

            get_title = g.find("div", class_="p-name p-name-type-2")
            get_a = get_title.find('a')
            get_detail['title'] = get_a['title']
            get_detail['url'] = get_a['href']

            get_com = g.find('div', class_='p-commit')
            get_com_a = get_com.find('a')
            get_detail['comm_num'] = get_com_a.get_text()
            id += 1
            get_detail['id'] = id

            detailCrawler(page, get_detail)
    except Exception as e:
        print(e)
        # with open(r'errorlist.txt', 'a', encoding='utf8') as f:
        #     f.write('page:' + str(page) + '\t' +
        #             'page error' + '\t' + str(e) + '\n')
        raise e
    # url, headers, data = buildheader(page)
    # r = requests.get(url=url, headers=headers, data=data)
    # s = BeautifulSoup(r.content, 'html.parser')
    # getgoods = s.find_all('li', class_='gl-item')


def main():
    for i in range(1, 101):
        reqweb(i)


if __name__ == '__main__':
    ts = dt.now()
    main()
    te = dt.now()
    tdif = te - ts
    print('[%s]' % tdif)
