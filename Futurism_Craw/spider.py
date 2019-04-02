from  urllib.parse import urlencode
import requests
import time
import json
import pymysql
from lxml import etree
import re
from Futurism_Craw.config import  *
from Futurism_Craw.data_filter import Data_Filter
from Futurism_Craw.mysql import MySQL

#对https://futurism.com 网站进行文章爬取，通过ajax请求返回数据，进行数据解析，结构化

from multiprocessing.pool import Pool
#the byte：https://futurism.com/wp-json/wp/v2/posts?tags[]=91937&page=2&per_page=12，page是变化的
#普通文章：https://futurism.com/wp-json/wp/v2/all-posts?exclude[]=155497&exclude[]=155513&exclude[]=155536&exclude[]=155522&filter[tag__not_in][]=91937&filter[tag__not_in][]=73328&page=2&per_page=12&show_on_homepage=true
#https://futurism.com/wp-json/wp/v2/all-posts?page=2&per_page=12


#爬虫模块
class Futurism_Spider():

    data_filter = Data_Filter()
    mysql = MySQL()

    latest_url = 'https://futurism.com/wp-json/wp/v2/all-posts?'
    byte_url = 'https://futurism.com/wp-json/wp/v2/posts?'

    headers_text = {
        'authority': 'futurism.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        'referer': 'https://futurism.com'
    }

    headers_byte = {
        'authority': 'futurism.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        'origin': 'https://futurism.com',
        'referer': 'https://www.futurism.com/the-byte'
    }

    # exclude[] = 155687 & exclude[] = 155649 & exclude[] = 155664 & exclude[] = 155640
    def get_latest_page(self,page):
        '''
        请求url，获取latest页json数据，然后睡眠5秒
        :param page: 第几页
        :return: json数据，为12条
        '''
        params = {
            'page': page,
            'per_page': '12',
            'filter[tag__not_in][]':73328,
            'show_on_homepage': 'true'
        }
        # 'filter[tag__not_in][]=91937&filter[tag__not_in][]=73328&page=1&per_page=12&show_on_homepage=true'
        #必须要这样写
        url = self.latest_url + urlencode(params) + '&filter%5Btag__not_in%5D%5B%5D=91937'
        # url = self.latest_url + 'filter%5Btag__not_in%5D%5B%5D=91937&filter%5Btag__not_in%5D%5B%5D=73328&page='+page+'&per_page=12&show_on_homepage=true'
        print(url)
        try:
            response = requests.get(url, headers=self.headers_text)
            if response.status_code == 200:
                # print(response.json()[0])
                return response.json()
        except requests.ConnectionError:
            return None
        finally:
            time.sleep(5)

    def get_byte_page(self,page):
        params = {
            'page': page,
            'per_page': '12',
            'tags[]': 91937
        }
        url = self.byte_url + urlencode(params)
        # url = self.byte_url + 'tags[]=91937&page=%d&per_page=12&show_on_homepage=true' % page
        print(url)
        try:
            response = requests.get(url, headers=self.headers_byte)

            if response.status_code == 200:
                # print(response.json()[0])
                return response.json()
        except requests.ConnectionError:
            return None
        finally:
            time.sleep(5)
        # 保存获取的信息保存到mysql中


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
            length = len(item) - 8
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
                'craw_time': item[7 + length].get('text')
            }
            self.mysql.insert(TARGET_TABLE,data)

        # self.mysql.close()


    def start(self,offset):

        #爬取latest页的数据
        json_latest = self.get_latest_page(offset)

        # print(len(json_latest))

        # 爬取byte页的数据
        json_byte = self.get_byte_page(offset)

        #对爬取的latest页的数据进行清洗
        latest_records = self.data_filter.get_futurism_infos(json_latest)
        #对爬取的latest页的数据进行存储
        self.data_converter_save(latest_records)
        # print(latest_records)

        print('=========='*10)
        # 对爬取的byte页的数据进行清洗
        byte_records = self.data_filter.get_futurism_infos(json_byte)
        # 对爬取的byte页的数据进行存储
        self.data_converter_save(byte_records)


        # print(byte_records)


    def run(self,offset):
        self.start(offset)

#多线程下载
if __name__ == '__main__':
    # main(1)
    fs = Futurism_Spider()
    for x in range(GROUP_START,GROUP_END + 1):
        fs.run(x * OFF_SET)
        # time.sleep(10)

    # 关闭数据库连接
    fs.mysql.close()



    # pool = Pool()
    # groups = ([x * OFF_SET for x in range(GROUP_START,GROUP_END + 1)])
    # pool.map(fs.run,groups)
    # pool.close()
    # pool.join()

