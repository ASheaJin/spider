#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a schedule module '

__author__ = 'Shea Jin'
import sys
sys.path.append('../')  # 新加入的
import datetime
import time
from Futurism_Craw.spider import *
from Futurism_Craw.config import *
from Futurism_Craw.publish import Publish
from Log_Module.my_logger import Logger

class Schedule():



    def __init__(self):
        self.spider = Futurism_Spider()
        self.publish = Publish()


    def doCraw(self):
        # 把爬虫程序放在这个类里
        for x in range(GROUP_START, GROUP_END + 1):
            self.spider.run(x * OFF_SET)

        time.sleep(60)

    def doPublish_hours(self):
        self.publish.main_hours()
        time.sleep(10)

    def doPublish_day(self):
        self.publish.main_yesterday()
        time.sleep(10)


    # 一般网站都是1:00点更新数据，所以每天凌晨一点启动
    def main_day(self,craw_h, craw_m,publish_h,publish_m):
        while True:
            while True:
                now = datetime.datetime.now()
                # print(now.hour, now.minute)
                #查看是否到爬取时间
                if now.hour == craw_h and now.minute == craw_m:
                    break
                #查看是否到发布时间，发布的是前一天前2条文章
                if (now.hour == publish_h or now.hour == publish_h + 4 or now.hour == publish_h + 10) and publish_m == 0:
                    self.doPublish_day()
                    # pass
                # 每隔60秒检测一次
                time.sleep(60)
            self.doCraw()


        # 一般网站都是1:00点更新数据，所以每天凌晨一点启动

    def main_hours(self, craw_m, publish_m):
        while True:
            while True:
                now = datetime.datetime.now()
                # print(now.hour, now.minute)
                # 查看是否到爬取时间
                if  now.minute == craw_m:
                    break
                # 查看是否到发布时间，发布的是前一天前3条文章
                if now.minute == publish_m:
                    self.doPublish_hours()
                # 每隔60秒检测一次
                time.sleep(60)

            self.doCraw()


if __name__ == '__main__':
    schedule = Schedule()
    #策略是每天凌晨1点爬取，每天8点30发2篇文章
    schedule.main_day(CARW_H,CARW_M,PUBLISH_H,PUBLISH_M)
    # schedule.main_hours(CARW_M,PUBLISH_M)