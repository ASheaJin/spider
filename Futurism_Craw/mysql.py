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

    def insert(self, table, data):
        """
        插入数据
        :param table:
        :param data:
        :return:
        """
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql_query = 'insert into %s (%s) values (%s)' % (table, keys, values)
        try:
            if self.cursor.execute(sql_query, tuple(data.values())):
                print('数据写入成功')
                self.db.commit()
        except:
            print('Failed')
            self.db.rollback()



    def select(self, table, columns, filter):

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
