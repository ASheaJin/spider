
# -*- coding:utf-8 -*-
#从数据库获取文章，发布文章，然后设置发布字段为1
import pymysql
from Futurism_Craw.config import *
from Futurism_Craw.mysql import MySQL
import requests
import time
import json

# SELECT
# 	url,
# 	release_time,
# 	pure_text
# FROM
# 	tb_article
# WHERE
# 	TO_DAYS(release_time) = TO_DAYS(NOW()) - 1

class Publish:
    mysql = MySQL()
    url = 'https://application.t.email/piper/spider/send'
    url_test = 'http://httpbin.org/post'

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',

    }

    data = {
        'content': '无内容',
        'piperTemail': 'p.20000026@msgseal.com',
        'token':'d9544a52744da2c0'
    }

    def publish(self,results):
        for article in results:
            pure_text = article[2]
            print(pure_text)
            self.data['content'] = pure_text
            try:
                #这里必需用json发送或者参考https://www.cnblogs.com/insane-Mr-Li/p/9145152.html
                r = requests.post(url=self.url, headers = self.headers, json= self.data)
                # r = requests.post(url=self.url, headers = self.headers, data= json.dumps(self.data))
                print(r.status_code)

                #如果发布成功，就回数据库中设置published = 1
                #这里必需加  \",否则查询语句就为update tb_article set published = 1 where url = https://futurism.com/russia-new-shotgun-wielding-drone-action/
                if r.status_code == 200:
                    self.mysql.update(TARGET_TABLE,'published = 1','url = \"' + article[0] + '\"')
            except:
                pass
            # print(r.text)
            time.sleep(3)

    def publishtest(self):
            # self.data['content'] = pure_text

            #这里必需用json发送或者参考https://www.cnblogs.com/insane-Mr-Li/p/9145152.html
            r = requests.post(url=self.url, headers = self.headers, json= self.data)
            print(r.status_code)

            #如果发布成功，就回数据库中设置published = 1
            #这里必需加  \",否则查询语句就为update tb_article set published = 1 where url = https://futurism.com/russia-new-shotgun-wielding-drone-action/
            if r.status_code == 200:
                # self.mysql.update(TARGET_TABLE,'published = 1','url = \"' + article[0] + '\"')
                pass
            # print(r.text)
            time.sleep(3)


    def set_token(self):

        pass

    def get_text_yesterday(self):
        columns = ['url','release_time','pure_text']
        #选取发布时间为昨天的文章,前3篇文章
        filter = 'TO_DAYS(release_time) = TO_DAYS(NOW()) - 1 and published = 0 limit 3'
        results = self.mysql.select(TARGET_TABLE,columns,filter)
        print(results)
        return results

        # return results

    def get_text_hours(self):
        columns = ['url', 'release_time', 'pure_text']
        # 选取发布时间为当前时间前一小时的文章
        # filter = 'TO_DAYS(release_time) = TO_DAYS(NOW()) - 1 and published = 0'
        filter = 'release_time BETWEEN ( NOW( ) - INTERVAL 1 DAY - INTERVAL 2 HOUR ) AND ( NOW( ) - INTERVAL 1 DAY ) and published = 0'
        results = self.mysql.select(TARGET_TABLE, columns, filter)
        print(results)
        return results

    def main_yesterday(self):
        self.mysql.get_connection()

        results = self.get_text_yesterday()
        print(results)
        self.publish(results)

        self.mysql.close_connection()

    def main_hours(self):
        self.mysql.get_connection()

        results = self.get_text_hours()
        print(results)
        self.publish(results)

        self.mysql.close_connection()

if __name__ == '__main__':
    pb = Publish()
    # pb.mysql.get_connection()
    # pb.main_yesterday()
    pb.main_hours()


    # pb.publishtest()
    # pb.mysql.close_connection()
