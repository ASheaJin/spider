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
from Log_Module.my_logger import Logger
from Futurism_Craw import short_url as su

# SELECT
# 	url,
# 	release_time,
# 	pure_text
# FROM
# 	tb_article
# WHERE
# 	TO_DAYS(release_time) = TO_DAYS(NOW()) - 1

class Publish():


    def __init__(self):
        self.logger = Logger(LOGGER_NAME).getlog()

        self.mysql = MySQL()
        self.url = PUBLISH_URL
        self.url_test = 'http://httpbin.org/post'

        self.headers = {
            'Content-Type': 'application/json'
        }

        self.data = {
            'content': '无内容',
            'piperTemail': PUBLISH_MAIL,
            'token': PUBLISH_TOKEN
        }

        self.complex_data = {
          "imgUrl": "string",
          "piperTemail": PUBLISH_MAIL,
          "title": "string",
          "token": PUBLISH_TOKEN,
          "txt": "详情",
          "url": "string"
        }


    def publish(self,results):
        for article in results:
            # pure_text = article[2]
            id = article[0] * 12
            link = ARTICLT_LINK + str(id)
            self.logger.debug('标题为: %s 链接为: %s' % (article[1],link))

            link = su.Convert_SINA_Short_Url(SOURCE,link)
            # self.data['content'] = '%s \n %s' % (article[1],link)
            self.complex_data['title'] = article[1]
            self.complex_data['imgUrl'] = article[2]
            self.complex_data['url'] = link
            print(self.complex_data)
            try:
                #这里必需用json发送或者参考https://www.cnblogs.com/insane-Mr-Li/p/9145152.html
                # r = requests.post(url=self.url, headers = self.headers, json= self.data)
                r = requests.post(url=self.url, headers = self.headers, json= self.complex_data)
                # r = requests.post(url=self.url, headers = self.headers, data= json.dumps(self.data))
                self.logger.debug(r.status_code)

                #如果发布成功，就回数据库中设置published = 1
                #这里必需加  \",否则查询语句就为update tb_article set published = 1 where url = https://futurism.com/russia-new-shotgun-wielding-drone-action/
                if r.status_code == 200:
                    self.mysql.update(TARGET_TABLE, 'published = 1', 'id = ' + str(article[0]))
            except:
                self.logger.error('发布文章失败，requests.post方法出现异常')
            # 设置文章之间发布间隔
            time.sleep(3)

    def get_text_yesterday(self):
        '''
        选取文章发布时间为前一周的文章里面随机两篇
        :return:
        '''
        columns = ['id','title','img_url']
        filter = 'DATE_SUB(CURDATE(), INTERVAL 7 DAY) <= date(release_time) and published = 0 limit 2'
        results = self.mysql.select(TARGET_TABLE,columns,filter)
        print(results)
        return results

    def get_text_hours(self):
        columns = ['url', 'release_time', 'pure_text']
        # 选取发布时间为当前时间前一小时的文章
        # filter = 'TO_DAYS(release_time) = TO_DAYS(NOW()) - 1 and published = 0'
        results = self.mysql.select(TARGET_TABLE, columns, PUBLISH_FILTER_BY_HOURS)

        return results

    def main_publishLastDay(self):
        if self.mysql.get_connection():
            try:
                results = self.get_text_yesterday()
                self.publish(results)
            finally:
                self.mysql.close_connection()

    def main_hours(self):
        #如果获取链接成功
        if self.mysql.get_connection():
            results = self.get_text_hours()
            print(results)
            self.publish(results)
            self.mysql.close_connection()

if __name__ == '__main__':
    pb = Publish()
    # pb.mysql.get_connection()
    pb.main_publishLastDay()
    # pb.main_hours()


    # pb.publishtest()
    # pb.mysql.close_connection()
