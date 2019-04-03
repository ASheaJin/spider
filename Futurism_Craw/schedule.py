# coding:utf8
import datetime
import time
from Futurism_Craw.spider import *
from Futurism_Craw.config import *
from Futurism_Craw.publish import Publish

class Schedule():

    def __init__(self):
        self.spider = Futurism_Spider()
        self.publish = Publish()


    def doCraw(self):
        # 把爬虫程序放在这个类里
        for x in range(GROUP_START, GROUP_END + 1):
            self.spider.run(x * OFF_SET)

        time.sleep(10)

    def doPublish(self):
        self.publish.main()
        time.sleep(10)



    # 一般网站都是1:00点更新数据，所以每天凌晨一点启动
    def main(self,craw_h, craw_m,publish_h,publish_m):
        while True:
            while True:
                now = datetime.datetime.now()
                # print(now.hour, now.minute)
                #查看是否到爬取时间
                if now.hour == craw_h and now.minute == craw_m:
                    break
                #查看是否到发布时间，发布的是前一天前3条文章
                if now.hour == publish_h and now.minute == publish_m:
                    self.doPublish()
                # 每隔60秒检测一次
                time.sleep(60)

            self.doCraw()



if __name__ == '__main__':
    schedule = Schedule()
    schedule.main(CARW_H,CARW_M,PUBLISH_H,PUBLISH_M)
