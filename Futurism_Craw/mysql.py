#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a mysql module '

__author__ = 'Shea Jin'
import sys
sys.path.append('../')  # 新加入的
import pymysql
from Futurism_Craw.config import  *
from Log_Module.my_logger import Logger

#存储模块
class MySQL():


    def __init__(self):
        self.logger = Logger(LOGGER_NAME).getlog()

        self.host = MYSQL_HOST
        self.username = MYSQL_USER
        self.password = MYSQL_PASSWORD
        self.port = MYSQL_PORT
        self.database = MYSQL_DATABASE

    def get_connection(self):
        try:
            self.db = pymysql.connect(self.host, self.username, self.password, self.database, charset='utf8', port=self.port)
            self.cursor = self.db.cursor()
            self.logger.info('获取数据库链接成功')
            return True
        # except pymysql.MySQLError as e:
        #     self.logger.debug(e.args)
        except Exception as e:
            self.logger.error('获取数据库链接失败', exc_info=True)
            return False


    def close_connection(self):

        try:
            if self.db:
                self.db.close()
                self.logger.info('关闭数据库链接成功')
                return True
        except Exception as e:
            self.logger.error('关闭数据库链接失败', exc_info=True)
            return False


    #插入的时候要判断这个url是否在数据库中
    def insert(self, table, data):
        """
        插入数据
        :param table:
        :param data:
        :return:
        """
        # self.select(table,data)

        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))

        sql_query = 'insert into %s (%s) values (%s)' % (table, keys, values)
        # self.logger.debug(self.select(table, 'count(url)', 'url = \"' + data.get('url') + '\"'))
        try:
             #判断要插入的数据是否在数据库中存在，按照url查询
            if self.select(table,'count(url)', 'url = \"' + data.get('url') + '\"') == ((0,),):
                if self.cursor.execute(sql_query, tuple(data.values())):
                    # self.logger.debug(self.select(table,'count(url)', 'url = \"' + data.get('url') + '\"'))
                    self.logger.info('数据插入成功')
                    self.db.commit()
            else:
                self.logger.info('数据库中该数据已经存在，插入失败')

        except Exception as e:
            self.logger.error('插入方法出现异常，数据插入失败', exc_info=True)
            self.db.rollback()



    def select(self, table, columns, filter):

        #如果类型为list类型，就要拼接
        if type(columns) == type([1,2]):
        # if isinstance(columns,list):
            columns = ', '.join(columns)

        sql_query = 'select %s from %s where %s' % (columns, table, filter)
        self.logger.info('查询语句为: %s' % sql_query)
        try:
            self.cursor.execute(sql_query)
            self.logger.info('查询出的数量：',self.cursor.rowcount)
            results = self.cursor.fetchall()
            return results
        except Exception as e:
            self.logger.error('查询方法出现异常',exc_info=True)


    def update(self,table,setter,filter):
        sql_query = 'update %s set %s where %s' % (table,setter,filter)
        self.logger.info(sql_query)
        try:
            self.cursor.execute(sql_query)
            self.logger.info('更新成功')
            self.db.commit()
        except Exception as e:
            self.logger.error('更新方法出现异常', exc_info=True)
            self.db.rollback()


if __name__ == '__main__':
    mysql = MySQL()
    mysql.get_connection()
    # mysql.update(TARGET_TABLE,'published = 1','url = ' + '\"https://futurism.com/russia-new-shotgun-wielding-drone-action/\"')
    if mysql.close_connection():
        self.logger.info('haha')
