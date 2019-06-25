#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a logger module '

__author__ = 'Shea Jin'

import logging
import logging.handlers
import sys
sys.path.append('../')  # 新加入的

# 开发一个日志系统， 既要把日志输出到控制台， 还要写入日志文件
class Logger():
    def __init__(self, logger):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # 创建 handler 输出到文件
        handler = logging.FileHandler("file.log", mode='a', encoding='utf-8')
        handler.setLevel(logging.INFO)

        # handler 输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # 创建 logging format
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        ch.setFormatter(formatter)

        # add the handlers to the logger
        self.logger.addHandler(handler)
        self.logger.addHandler(ch)

    def getlog(self):
        return self.logger

    # @classmethod
    # def test(self):
    #     print('hah')

if __name__ == '__main__':
    logger = Logger("Shea").getlog()
    try:
        1 / 0
    except Exception as e:
        logger.error("wrong! ", exc_info=True)

    print('token')

    # Logger.test()
