# -*- coding:utf-8 -*-

import pymysql
from Futurism_Craw.config import  *
import json

#存储模块
class MySQL():
    host = MYSQL_HOST
    username = MYSQL_USER
    password = MYSQL_PASSWORD
    port = MYSQL_PORT
    database = MYSQL_DATABASE

    def __init__(self):
        pass

    def get_connection(self):
        try:
            self.db = pymysql.connect(self.host, self.username, self.password, self.database, charset='utf8', port=self.port)
            self.cursor = self.db.cursor()
        except pymysql.MySQLError as e:
            print(e.args)


    def close_connection(self):
        if self.db:
            self.db.close()

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
        # print(self.select(table, 'count(url)', 'url = \"' + data.get('url') + '\"'))
        try:
             if self.select(table,'count(url)', 'url = \"' + data.get('url') + '\"') == ((0,),):
                if self.cursor.execute(sql_query, tuple(data.values())):
                    # print(self.select(table,'count(url)', 'url = \"' + data.get('url') + '\"'))
                    print('数据写入成功')
                    self.db.commit()

        except:
            print('Failed')
            self.db.rollback()



    def select(self, table, columns, filter):

        #如果类型为list类型，就要拼接
        if type(columns) == type([1,2]):
            columns = ', '.join(columns)

        sql_query = 'select %s from %s where %s' % (columns, table, filter)
        print(sql_query)
        try:
            self.cursor.execute(sql_query)
            print('查询出的数量：',self.cursor.rowcount)
            results = self.cursor.fetchall()
            return results
        except:
            print('查询失败')


    def update(self,table,setter,filter):
        sql_query = 'update %s set %s where %s' % (table,setter,filter)
        print(sql_query)
        try:
            self.cursor.execute(sql_query)
            print('success')
            self.db.commit()
        except:
            print('failed')
            self.db.rollback()


if __name__ == '__main__':
    mysql = MySQL()
    mysql.get_connection()
    mysql.update(TARGET_TABLE,'published = 1','url = ' + '\"https://futurism.com/russia-new-shotgun-wielding-drone-action/\"')
    mysql.close_connection()
