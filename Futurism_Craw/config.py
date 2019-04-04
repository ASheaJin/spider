# -*- coding:utf-8 -*-


#存放常用静态变量和数据库链接

#ajax请求规律参数
GROUP_START = 1
GROUP_END = 1

OFF_SET = 1

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
CARW_H = 19
CARW_M = 15

#规定发布文章时间
PUBLISH_H = 19
PUBLISH_M = 20

#添加订阅号
piperTemail = ''