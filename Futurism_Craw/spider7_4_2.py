from  urllib.parse import urlencode
import requests
import time
import json
import pymysql
from lxml import etree
import re

#对https://futurism.com 网站进行文章爬取，通过ajax请求返回数据，进行数据解析，结构化

from multiprocessing.pool import Pool
#the byte：https://futurism.com/wp-json/wp/v2/posts?tags[]=91937&page=2&per_page=12，page是变化的
#普通文章：https://futurism.com/wp-json/wp/v2/all-posts?exclude[]=155497&exclude[]=155513&exclude[]=155536&exclude[]=155522&filter[tag__not_in][]=91937&filter[tag__not_in][]=73328&page=2&per_page=12&show_on_homepage=true
#https://futurism.com/wp-json/wp/v2/all-posts?page=2&per_page=12

class Futurism_Spider():

    latest_url = 'https://futurism.com/wp-json/wp/v2/all-posts?'
    byte_url = 'https://futurism.com/wp-json/wp/v2/posts?'

    headers_text = {
        'authority':'futurism.com',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        'x-requested-with':'XMLHttpRequest',
        'referer':'https://futurism.com'
    }

    headers_byte = {
        'authority': 'futurism.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        'origin': 'https://futurism.com',
        'referer':'https://www.futurism.com/the-byte'
    }

    GROUP_START = 1
    GROUP_END = 1
    OFF_SET = 1

    # exclude[] = 155687 & exclude[] = 155649 & exclude[] = 155664 & exclude[] = 155640
    def get_latest_page(self,page):
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

    def get_byte_page(self,page):
        params = {
            'page': page,
            'per_page': '12',
            'tags[]': 91937
        }
        url = self.byte_url + urlencode(params)
        # url = self.byte_url + 'tags[]=91937&page=%d&per_page=12&show_on_homepage=true' % page
        try:
            response = requests.get(url, headers=self.headers_byte,params = params)
            if response.status_code == 200:
                # print(response.json()[0])
                return response.json()
        except requests.ConnectionError:
            return None


    # src（源）
    # # url
    # # title
    # # content
    # # author
    # # createtimes
    # # crawtimes
    # # others
    # # data  --  仿造showtype格式

    def get_futurism_infos(self,json):
        for page_num in range(12):

            if json[page_num]:
                item = json[page_num]
                #文章标题
                title = item.get('title').get('plain_text')
                #文章正文
                content = item.get('content').get('rendered')
                #文章url
                article_url = item.get('link')
                #文章作者
                author = item.get('author_detailed').get('display_name')
                #文章发布时间
                release_time = item.get('modified')
                release_time = release_time.replace('T',' ')
                #爬取时间
                craw_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                #文章来源网站
                source_sit_url = 'https://futurism.com'

                img_url = item.get('featured_image').get('url')

                # print(img_url)
                content_list = self.content_parse(content)

                article_text = [
                    {
                        'type': 6,
                        'text': source_sit_url
                    },
                    {
                        'type': 6,
                        'text': article_url
                    },
                    {
                        'type': 1,
                        'imageUrl': img_url
                    },
                    {
                        'type': 5,
                        'text': title
                    },
                    {
                        'type': 0,
                        'text': author
                    }]

                article_text = article_text + content_list

                article_text.append({
                    'type': 0,
                    'text': release_time
                })
                article_text.append({
                    'type': 0,
                    'text': craw_time
                })

                # print(article_text)
                print(page_num)
                yield article_text

        #"type":"int    0表示文本，1图片 2地图 3小视频，4语音 5 标题 6 链接",

    #对正文进行解析，最后返回正文解析的数组字典
    def content_parse(self,content):
        content_html = etree.HTML(content)
        print('content_parse ======='*5)
        print(content)
        print('+++++++++' * 5)
        youtubu = content_html.xpath('//iframe/@src')
        print(len(youtubu))

        text_list = []
        #如果里面没有youtub 的视频
        if len(youtubu) == 0:
            str_text = content_html.xpath('//body//text()')
            print(str_text)
            temp = ''
            for str in str_text:
                if str.startswith('https://') or str.startswith('http://'):
                    text_list.append(temp)
                    text_list.append(str)
                    temp = ''
                elif 'READ MORE' in str:
                    break
                else:
                    temp = temp + str

            text_list.append(temp)

            print(text_list)
        else:
            video_list = content_html.xpath('//iframe/@src')
            i = 0
            node_list = content_html.xpath('//body//*')
            print(node_list)
            temp = ''
            for node in node_list:
                if node.tag != 'iframe':
                    if node.text is not None:
                        temp = temp + node.text
                else:
                    text_list.append(temp)
                    text_list.append(video_list[i])
                    i = i + 1
                    temp = ''
            temp = temp.split('READ MORE:')[0]
            text_list.append(temp)
            print(text_list)

        content_list = []
        content_dic = {}
        for build in text_list:
            if build.startswith('http'):
                content_dic['type'] = 3
            else:
                content_dic['type'] = 0
            content_dic['text'] = build
            print(content_dic)
            content_list.append(content_dic)
            content_dic = {}
        print('|||||||||||||||||||||||||')
        print(content_list)

        return content_list


    # 保存获取的信息保存到mysql中
    def save_info_Mysql(self,records):
        db = pymysql.connect(host='localhost', user='root', password='root', port=3306, db='sprider')
        cursor = db.cursor()
        cursor.execute('select version()')
        data2 = cursor.fetchone()
        print('database version:', data2)

        for item in records:
            #动态的content大小
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
            table = 'tb_article'
            keys = ','.join(data.keys())
            values = ','.join(['%s'] * len(data))
            sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table = table,keys = keys,values = values)

            try:
                if cursor.execute(sql,tuple(data.values())):
                    print('数据写入成功')
                    db.commit()
            except:
                print('Failed')
                db.rollback()

        db.close()


    def start(self,offset):

        json_latest = self.get_latest_page(offset)
        print(len(json_latest))
        json_byte = self.get_byte_page(offset)

        latest_records = self.get_futurism_infos(json_latest)
        self.save_info_Mysql(latest_records)
        # print(latest_records)

        print('=========='*10)
        byte_records = self.get_futurism_infos(json_byte)
        self.save_info_Mysql(byte_records)
        # print(byte_records)

    def run(self,offset):
        self.start(offset)

#多线程下载
if __name__ == '__main__':
    # main(1)
    fs = Futurism_Spider()
    # fs.run(1)
    pool = Pool()
    groups = ([x * fs.OFF_SET for x in range(fs.GROUP_START,fs.GROUP_END + 1)])
    pool.map(fs.run,groups)
    pool.close()
    pool.join()

