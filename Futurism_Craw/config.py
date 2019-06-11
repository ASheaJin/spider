#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a config module '

__author__ = 'Shea Jin'

#存放常用静态变量和数据库链接

#ajax请求规律参数
GROUP_START = 1
GROUP_END = 1

# OFF_SET = 1

PER_PAGE = 12

#数据库的基本信息
MYSQL_HOST = '172.28.50.12'

MYSQL_PORT = 3306

MYSQL_USER = 'root'

MYSQL_PASSWORD = '9A7FEa98sP'

MYSQL_DATABASE = 'spider'
#要插入的表
TARGET_TABLE = 'tb_article'


# #数据库的基本信息
# MYSQL_HOST = 'localhost'
#
# MYSQL_PORT = 3306
#
# MYSQL_USER = 'root'
#
# MYSQL_PASSWORD = 'root'
#
# MYSQL_DATABASE = 'sprider'
# #要插入的表
# TARGET_TABLE = 'tb_article'

#   "type":int    0表示文本，1图片 2地图 3小视频，4语音 5 标题 6 链接"
TEXT = 0
IMAGE = 1
MAP = 2
VEDIO = 3
VOICE = 4
TITLE = 5
LINK = 6

#规定爬取时间
CARW_H = 1
CARW_M = 10

#规定发布文章时间
PUBLISH_H = 8
PUBLISH_M = 0

#添加订阅号
# PUBLIST_URL = 'https://application.t.email/piper/spider/send'
PUBLISH_URL = 'https://application.t.email/piper/spider/sendComplexInfo'
PUBLISH_TOKEN = 'd9544a52744da2c0'
PUBLISH_MAIL = 'p.20000026@msgseal.com'



#添加filter
PUBLISH_FILTER_BY_HOURS = 'release_time BETWEEN ( NOW( ) - INTERVAL 1 DAY - INTERVAL 24 HOUR ) AND ( NOW( ) - INTERVAL 1 DAY ) and published = 0'

LOGGER_NAME = 'Shea'

ARTICLT_LINK = 'https://application.t.email/pages/article/'

#我的App Key:828375184
SOURCE = '828375184'


# 得到app参数
DEDAO_ARTICLT_LINK = 'https://application.t.email/pages/dedao_article/'


# 得到app订阅号信息
# DEDAO_PUBLIST_URL = 'https://application.t.email/piper/spider/send'
DEDAO_PUBLISH_URL = 'https://application.t.email/piper/spider/sendComplexInfo'
DEDAO_PUBLISH_TOKEN = '223cceafd35557ba'
DEDAO_PUBLISH_MAIL = 'p.20000001@msgseal.com'

DEDAO_PUBLISH_HOUR = 8
DEDAO_PUBLIST_MIN = 0


TEST_PUBLISH_URL = 'http://172.31.241.102:8080/piper/spider/sendComplexInfo'
TEST_PUBLISH_TOKEN = 'd9544a52744da2c0'
TEST_PUBLISH_MAIL = 'p.10000001@t.email'
