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
            self.spider.run(x)

    def doPublish_day(self):
        self.publish.main_publishLastDay()

    # 一般网站都是1:00点更新数据，所以每天凌晨一点启动
    def main_day(self,craw_h, craw_m,publish_h,publish_m):

        while True:
            now = datetime.datetime.now()
            #查看是否到爬取时间，爬取时间为1:10
            if now.hour == craw_h and now.minute == craw_m:
                self.doCraw()
            #发布时间是每天8:00,19:00，发布最近一周的未被发布过的两篇文章
            if (now.hour == publish_h or now.hour == publish_h + 11) and now.minute == publish_m:
                self.doPublish_day()
            # 每隔60秒检测一次
            time.sleep(60)


if __name__ == '__main__':
    schedule = Schedule()
    # 进行未来主义的一天的发布和爬取策略
    # schedule.main_day(CARW_H,CARW_M,PUBLISH_H,PUBLISH_M)
    schedule.main_day(CARW_H,CARW_M,9,18)
    # schedule.main_hours(CARW_M,PUBLISH_M)