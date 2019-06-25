#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a publish module '

__author__ = 'Shea Jin'
#从数据库获取文章，发布文章，然后设置发布字段为1
import sys
sys.path.append('../')  # 新加入的
from Futurism_Craw.config import *
from Futurism_Craw.mysql import MySQL
import requests
import time
import pickle
from Log_Module.my_logger import Logger
from Futurism_Craw import short_url as su
import os
from Dedao_Craw import add_article

class Dedao_Publish():

    def __init__(self):
        self.logger = Logger(LOGGER_NAME).getlog()

        self.mysql = MySQL()
        self.url = DEDAO_PUBLISH_URL
        # self.url = TEST_PUBLISH_URL
        self.url_test = 'http://httpbin.org/post'

        self.headers = {
            'Content-Type': 'application/json'
        }

        self.data = {
            'content': '无内容',
            'piperTemail': DEDAO_PUBLISH_MAIL,
            'token': DEDAO_PUBLISH_TOKEN
        }

        self.complex_data = {
            "imgUrl": "string",
            "piperTemail": DEDAO_PUBLISH_MAIL,
            # "piperTemail": TEST_PUBLISH_MAIL,
            "title": "string",
            "token": DEDAO_PUBLISH_TOKEN,
            # "token": TEST_PUBLISH_TOKEN,
            "txt": "详情",
            "url": "string",
            'imgTxt':''
        }


    def dedao_publish(self,publish_info):
        link = DEDAO_ARTICLT_LINK + str(publish_info.get('article_id'))
        print(link)
        short_link = su.Convert_SINA_Short_Url(SOURCE, link)

        self.complex_data['imgUrl'] = publish_info.get('cover_image')
        self.complex_data["imgTxt"] = publish_info.get('article_name')
        self.complex_data["url"] = short_link
        self.complex_data["title"] = publish_info.get('column_name')

        print(self.complex_data)
        try:
            # 这里必需用json发送或者参考https://www.cnblogs.com/insane-Mr-Li/p/9145152.html
            r = requests.post(url=self.url, headers=self.headers, json=self.complex_data)

            if r.status_code == 200:
                self.mysql.update('article', 'published = 1', 'article_id = ' + str(publish_info.get('article_id')))

                filter = "article_id = " + str(publish_info.get('article_id')) + " and attribute_name = 'next_article_id'"
                result_next_id = self.mysql.select('ext_attribute', ['article_id','attribute_name','attribute_value'], filter)

                with open('1.txt', 'rb') as f:
                    temp = pickle.load(f)
                with open('1.txt', 'wb') as f:
                    f.truncate()

                temp[int(publish_info.get('index'))] = {'next_article_id': result_next_id[0][2]}

                # 把下一篇文章id添加到文件
                with open('1.txt', 'wb') as f:
                    pickle.dump(temp, f)


        except Exception as e:
            self.logger.error('发布文章失败，requests.post方法出现异常',exc_info=True)
        # 文章之间发布间隔
        time.sleep(3)


    def get_dedao_article(self, id, index):

        # 查询出栏目名称，章节名称，还需要进行上一篇文章，下一篇文章的判断
        # 如果从外界传入 0 ，说明需要找新的栏目了，不为0就是老栏目
        # 如果为新栏目，需要返回当前信息，还需要返回下一篇文章的article_id
        # 如果为老栏目，需要返回当前信息，还需要返回下一篇文章的article_id
        if int(id):
            filter = "published = 0 and article_id = " + str(id)
        else:
            filter = "published = 0 and article_id in (select article_id from ext_attribute where attribute_name = 'prev_article_id' and attribute_value = '0') limit 1"
        # 得到当前文章的信息,文章id，文章名字
        columns_article = ['id', 'article_id', 'article_name']
        results = self.mysql.select('article', columns_article, filter)
        cur_article_id = str(results[0][1])

        # 得到当前文章的下一篇文章的id
        columns_ext_attribute = ['article_id','attribute_name','attribute_value']


        # 得到当前文章的章节名
        filter = "article_id = " + cur_article_id + " and attribute_name = 'chapter_name'"
        result_chapter_name = self.mysql.select('ext_attribute', columns_ext_attribute, filter)

        # 得到当前文章的封面
        filter = "article_id = " + cur_article_id + " and attribute_name = 'cover_image'"
        result_cover_image = self.mysql.select('ext_attribute', columns_ext_attribute, filter)

        # 得到当前文章的栏目名
        columns_column = ['column_id','column_name','column_info']
        filter = "column_id in (select column_id from article_column where article_id = "+cur_article_id+")"
        result_column_name = self.mysql.select('tb_column', columns_column, filter)
        # print(result_column_name)


        publish_info = {}
        publish_info['article_id'] = results[0][1]
        publish_info['column_name'] = result_column_name[0][1]
        publish_info['chapter_name'] = result_chapter_name[0][2] if result_chapter_name else ''
        publish_info['article_name'] = results[0][2]
        publish_info['cover_image'] = result_cover_image[0][2] if result_cover_image else ''
        publish_info['index'] = index

        # print(publish_info)
        return publish_info

    def schedule_dedao(self,id,index):
        try:
            self.mysql.get_connection()

            publish_info = self.get_dedao_article(id,index)
            # print(results)

            self.dedao_publish(publish_info)

        finally:
            self.mysql.close_connection()

if __name__ == '__main__':
    pb = Dedao_Publish()
    # pb.schedule_dedao(0)

    if os.path.exists('1.txt'):
        with open('1.txt', 'rb') as f:
            temp = pickle.load(f)
        # self.publish.schedule_dedao(temp.get('next_article_id'))
    else:
        with open('1.txt', 'wb') as f:
            temp = [{'next_article_id':0}]
            pickle.dump(temp,f)

    for index,item in enumerate(temp):
        print(item.get('next_article_id'))
        pb.schedule_dedao(item.get('next_article_id'), index)
