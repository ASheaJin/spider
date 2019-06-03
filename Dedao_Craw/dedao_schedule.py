#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a schedule module '

__author__ = 'Shea Jin'
import sys
sys.path.append('../')  # 新加入的
import datetime
import time
import os
from Dedao_Craw.dedao_publish import Dedao_Publish
from Futurism_Craw.config import *
from Log_Module.my_logger import Logger
import pickle

class Schedule():

    def __init__(self):
        self.publish = Dedao_Publish()

    def doPublish_day(self):
        if os.path.exists('1.txt'):
            with open('1.txt', 'rb') as f:
                temp = pickle.load(f)
            # self.publish.schedule_dedao(temp.get('next_article_id'))
        else:
            with open('1.txt', 'wb') as f:
                temp = [{'next_article_id': 0}]
                pickle.dump(temp, f)

        for index, item in enumerate(temp):
            # print(item.get('next_article_id'))
            self.publish.schedule_dedao(item.get('next_article_id'), index)

        time.sleep(10)

    # 一般网站都是1:00点更新数据，所以每天凌晨一点启动
    def main_day(self,dedao_publish_h,dedao_publish_m):
        while True:
            now = datetime.datetime.now()
            # print(now.hour, now.minute)
            #查看是否到发布时间
            if (now.hour == dedao_publish_h or now.hour == dedao_publish_h + 11) and now.minute == dedao_publish_m:
                self.doPublish_day()
                # pass
            # 每隔60秒检测一次
            time.sleep(60)


if __name__ == '__main__':
    schedule = Schedule()
    # 每天8，19点,发布文章
    schedule.main_day(DEDAO_PUBLISH_HOUR,DEDAO_PUBLIST_MIN)
    # schedule.main_hours(CARW_M,PUBLISH_M)