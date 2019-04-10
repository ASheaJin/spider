#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a logger module '

__author__ = 'Shea Jin'

import logging
import logging.handlers
import os
import sys
sys.path.append('../')  # 新加入的


#用字典保存日志级别
format_dict = {
   1 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
   2 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
   3 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
   4 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
   5 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
}
# 开发一个日志系统， 既要把日志输出到控制台， 还要写入日志文件
class Logger():
    def __init__(self, logger):
        '''
           指定保存日志的文件路径，日志级别，以及调用文件
           将日志存入到指定的文件中
        '''
        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.INFO)

        # 创建一个handler，用于写入日志文件
        # fh = logging.FileHandler(logname)
        # fh.setLevel(logging.DEBUG)
        if not os.path.exists('../log'):
            os.mkdir('../log')

        time_handler = logging.handlers.TimedRotatingFileHandler('../log/error.log', when='D', interval=1, backupCount=7)
        time_handler.suffix = '%Y-%m-%d.log'
        time_handler.setLevel(logging.WARNING)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        formatter = format_dict[5]
        time_handler.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(time_handler)
        self.logger.addHandler(ch)

    def getlog(self):
        return self.logger

if __name__ == '__main__':
    logger = Logger(logger="Shea").getlog()
    logger.error('wrong')
