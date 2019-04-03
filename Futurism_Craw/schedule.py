# coding:utf8
import datetime
import time
from Futurism_Craw.spider import *
from Futurism_Craw.config import *

class Schedule():

    def __init__(self):
        self.spider = Futurism_Spider()


    def doSth(self):
        # 把爬虫程序放在这个类里
        for x in range(GROUP_START, GROUP_END + 1):
            self.spider.run(x * OFF_SET)

        time.sleep(60)


    # 一般网站都是1:00点更新数据，所以每天凌晨一点启动
    def main(self,h, m):
        while True:
            while True:
                now = datetime.datetime.now()
                # print(now.hour, now.minute)
                if now.hour == h and now.minute == m:
                    break
                # 每隔60秒检测一次
                time.sleep(60)

            self.doSth()



if __name__ == '__main__':
    schedule = Schedule()
    schedule.main(H,M)
