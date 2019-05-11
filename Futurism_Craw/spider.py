#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a spider module '

__author__ = 'Shea Jin'

import sys
sys.path.append('../')  # 新加入的

from  urllib.parse import urlencode
import requests
import time
import json
from Futurism_Craw.config import *
from Futurism_Craw.data_filter import Data_Filter
from Futurism_Craw.mysql import MySQL
from Log_Module.my_logger import Logger
import random



#对https://futurism.com 网站进行文章爬取，通过ajax请求返回数据，进行数据解析，结构化

#the byte：https://futurism.com/wp-json/wp/v2/posts?tags[]=91937&page=2&per_page=12，page是变化的
#普通文章：https://futurism.com/wp-json/wp/v2/all-posts?exclude[]=155497&exclude[]=155513&exclude[]=155536&exclude[]=155522&filter[tag__not_in][]=91937&filter[tag__not_in][]=73328&page=2&per_page=12&show_on_homepage=true
#https://futurism.com/wp-json/wp/v2/all-posts?page=2&per_page=12


#爬虫模块
class Futurism_Spider():

    def __init__(self):
        self.data_filter = Data_Filter()
        self.mysql = MySQL()
        self.logger = Logger(LOGGER_NAME).getlog()

        self.latest_url = 'https://futurism.com/wp-json/wp/v2/all-posts?'
        self.byte_url = 'https://futurism.com/wp-json/wp/v2/posts?'

        self.headers_text = {
            'authority': 'futurism.com',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
            'referer': 'https://futurism.com',
            'authorization': 'Basic Z3V0ZW1iZXJnOnNQbWt5U2tzMTgx',
            'cookie': '_ga=GA1.2.313593188.1553562842; em_cdn_uid=t%3D1553562842379%26u%3D4b7cf968aa994279b21ccc876bfa9f66; __smVID=663baa57d0c6f2a259a337deca5bee866c8553fe1e372b71173b96cbe09517d3; __gads=ID=497970e128469b51:T=1553562844:S=ALNI_Mbyvt_dLSsVi-BUBPNE17tP0VdqaQ; __qca=P0-1687767503-1553562843711; __smListBuilderShown=Tue%20Mar%2026%202019%2009:14:20%20GMT+0800%20(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4); _fbp=fb.1.1554079490081.715629428; __smToken=BuS35jwAvnHhRIjyFOnsXWOI; _gid=GA1.2.818504779.1554684291'
        }

        self.headers_byte = {
            'authority': 'futurism.com',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
            # 'origin': 'https://futurism.com',
            'referer': 'https://www.futurism.com/the-byte',
            'authorization': 'Basic Z3V0ZW1iZXJnOnNQbWt5U2tzMTgx',
            'cookie': '_ga=GA1.2.313593188.1553562842; em_cdn_uid=t%3D1553562842379%26u%3D4b7cf968aa994279b21ccc876bfa9f66; __smVID=663baa57d0c6f2a259a337deca5bee866c8553fe1e372b71173b96cbe09517d3; __gads=ID=497970e128469b51:T=1553562844:S=ALNI_Mbyvt_dLSsVi-BUBPNE17tP0VdqaQ; __qca=P0-1687767503-1553562843711; __smListBuilderShown=Tue%20Mar%2026%202019%2009:14:20%20GMT+0800%20(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4); _fbp=fb.1.1554079490081.715629428; __smToken=BuS35jwAvnHhRIjyFOnsXWOI; _gid=GA1.2.818504779.1554684291'

        }

    # exclude[] = 155687 & exclude[] = 155649 & exclude[] = 155664 & exclude[] = 155640
    def get_latest_page(self,page,current_count = 1,req_count = 3):

        '''
        请求url，获取latest页json数据，然后睡眠5秒
        :param page: 第几页
        :return: json数据，为12条
        '''
        if current_count <= req_count:
            params = {
                'page': page,
                'per_page': '12',
                'filter[tag__not_in][]':73328,
                'show_on_homepage': 'true'
            }
            #必须要这样写
            url = self.latest_url + urlencode(params) + '&filter%5Btag__not_in%5D%5B%5D=91937'
            print('请求的url为:%s,这是请求的第%d次' % (url,current_count))

            try:
                #如果60秒没有响应，就抛出异常
                response = requests.get(url, headers=self.headers_text,timeout = 60)
                #如果请求成功
                if response.status_code == 200:
                    print('latest请求成功')
                    return response.json()
                else:
                    print('latest请求失败')
                    self.logger.error('Futurism_Craw ->spider.py-> get_latest_page()方法的latest请求失败，response.status_code != 200 url: %s' % url)
                    return None

            except requests.ConnectionError:
                print('再次连接访问！')
                self.logger.error('Futurism_Craw ->spider.py-> get_latest_page()方法的latest请求发送异常，可能是超时，再次连接访问！url: %s' % url)
                return self.get_latest_page(page,current_count + 1,req_count)
        else:
            print('latest请求超过限定次数')
            self.logger.error('Futurism_Craw ->spider.py-> get_latest_page()方法的latest请求失败，请求次数超过设定值:%d' % (req_count))
            return None



#
    def get_byte_page(self,page,current_count = 1,req_count = 3):
        if current_count <= req_count:
            params = {
                'page': page,
                'per_page': '12',
                'tags[]': 91937
            }
            url = self.byte_url + urlencode(params)
            print('请求的url为:%s,这是请求的第%d次' % (url,current_count))

            try:
                response = requests.get(url, headers=self.headers_byte)
                if response.status_code == 200:
                    return response.json()
                else:
                    print('byte请求失败')
                    self.logger.error('Futurism_Craw ->spider.py-> get_byte_page()方法的byte请求失败，response.status_code != 200 url: %s' % url)
                    return None
            except requests.ConnectionError:
                print('再次连接访问！')
                self.logger.error('byte中requests.get()方法发生异常，再次连接访问！url: %s' % url)
                return self.get_byte_page(page,current_count + 1,req_count)
        else:
            print('byte请求超过限定次数')
            self.logger.error('byte请求失败，请求次数超过设定值:%d' % (req_count))
            return None


    def data_converter_save(self, records):
        '''
        数据的转换和存储
        :param records: 为生成器，存放的是每条新闻结构化后的集合
        :return:
        '''
        # db = pymysql.connect(host='localhost', user='root', password='root', port=3306, db='sprider')
        # cursor = db.cursor()
        # cursor.execute('select version()')
        # data2 = cursor.fetchone()
        # print('database version:', data2)

        for item in records:
            # 动态的content大小

            #这里要改变，之前为-8，这里多了个pure_text
            length = len(item) - 9

            pure_text = item[8 + length].get('text')
            #这里item要改变一下，把里面除了pure_text的变为json
            #去除尾
            item.pop()
            json_data = json.dumps(item)

            data = {
                'url': item[1].get('text'),
                'src_url': item[0].get('text'),
                'img_url': item[2].get('imageUrl'),
                'title': item[3].get('text'),
                # 'content': item[4].get('text'),
                'author': item[4].get('text'),
                'data': json_data,
                'release_time': item[6 + length].get('text'),
                'craw_time': item[7 + length].get('text'),
                'pure_text': pure_text
            }
            self.mysql.insert(TARGET_TABLE,data)

    def start(self,offset):

        #爬取latest页的数据,请求超过3次还没返回就返回None
        json_latest = self.get_latest_page(offset,1,3)

        #请求的时间间隔为5秒
        time.sleep(random.randint(5,10))
        # print(len(json_latest))

        # 爬取byte页的数据
        json_byte = self.get_byte_page(offset,1,3)

        time.sleep(random.randint(5,10))

        #只要二者有一个不为None，就开启数据库连接
        if json_byte or json_latest:
            try:
                #优化：获取数据库连接
                if self.mysql.get_connection():
                    #如果请求到数据
                    if json_latest:
                        #对爬取到的latest页的数据进行清洗
                        latest_records = self.data_filter.get_futurism_infos(json_latest)

                        #对爬取到的latest页的数据进行存储
                        self.data_converter_save(latest_records)

                    if json_byte:
                        # 对爬取到的byte页的数据进行清洗
                        byte_records = self.data_filter.get_futurism_infos(json_byte)

                        # 对爬取到的byte页的数据进行存储
                        self.data_converter_save(byte_records)

            finally:
                #关闭数据库连接
                self.mysql.close_connection()


        else:
            print('这次爬取失败~~~~~~~~~~~~~~~~，未向数据库插入数据')
            self.logger.warning('当前时间的爬虫未能爬取到数据')


    def run(self,offset):
        self.start(offset)

#多线程下载
if __name__ == '__main__':

    # main(1)
    fs = Futurism_Spider()
    for x in range(GROUP_START,GROUP_END + 1):
        fs.run(x * OFF_SET)
        # time.sleep(10)

    # pool = Pool()
    # groups = ([x * OFF_SET for x in range(GROUP_START,GROUP_END + 1)])
    # pool.map(fs.run,groups)
    # pool.close()
    # pool.join()
