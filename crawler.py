# http://www.imooc.com/learn/712
# 部分代码笔记

from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import re
import requests
import pymysql
import pymysql.cursors


URL = 'https://en.wikipedia.org/wiki/Main_Page'
URL_QIUBAI = 'https://www.qiushibaike.com/8hr/page'
headers = {'User-Agent':
           'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}


# urllib.request.urlopen 方法
def url_get():
    resp = urlopen(URL).read().decode('utf-8')
    soup = bs(resp, 'html.parser')
    listURL = soup.findAll('a', href=re.compile('^/wiki/'))

    for url in listURL:
        if not re.search('\.(jpg|JPG)$', url['href']):
            print(url.get_text(), '<--->',
                  'https://en.wikipedia.org' + url['href'])


# requests 方法
def requests_get_wiki():
    resp = requests.get(URL, headers=headers)
    content = resp.text
    soup = bs(content, 'lxml')
    listURL = soup.findAll('a', href=re.compile('^/wiki/'))

    for url in listURL:
        # 排除图片内容
        if not re.search('\.(jpg|JPG)$', url['href']):
            print(url.get_text(), '<--->',
                  'https://en.wikipedia.org' + url['href'])
            # 本地 mysql 数据库
            connection = pymysql.connect(host='localhost',
                                         user='guest',
                                         password='1230',
                                         db='wikiurl',
                                         charset='utf8mb4')
            try:
                with connection.cursor() as cursor:
                    sql = "insert into `urls` (`urlname`, `urlhref`) values(%s, %s)"
                    cursor.execute(
                        sql, (url.get_text(), 'https://en.wikipedia.org' + url['href']))
                    connection.commit()
            finally:
                connection.close()


# 糗百百科
def requests_get():
    for i in range(1, 5):
        resp = requests.get(URL_QIUBAI + '/i', headers=headers)
        content = resp.text
        soup = bs(content, 'lxml')
        # print(soup)
        typelist = ('hot', 'old', 'long', 'recent')
        divs = []
        for i in typelist:
            divs_temp = soup.find_all(
                class_='article block untagged mb15 typs_{}'.format(i))
            divs = divs + divs_temp
        # print(divs)
        for div in divs:
            if div.find_all(class_='thumb'):
                continue
            joke = div.span.get_text()
            print(joke)
            print('-----')


# 读取数据库
def read_mysql():
    connection = pymysql.connect(host='localhost',
                                 user='guest',
                                 password='1230',
                                 db='wikiurl',
                                 charset='utf8mb4')

    try:
        with connection.cursor() as cursor:
            # 查看、输出数据数目
            sql = 'select `urlname`, `urlhref` from `urls` where `id` is not null'
            count = cursor.execute(sql)
            print(count)

            # 查看、输出所有数据
            # result = cursor.fetchall()
            # print(result)
    finally:
        connection.close()


if __name__ == '__main__':
    # url_get()

    # requests_get_wiki()

    # 读取数据库
    read_mysql()
