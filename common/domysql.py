import pymysql
from common.read_config import config


class DoMysql:

    def __init__(self):
        host = config.get_str('db', 'host')
        user = config.get_str('db', 'user')
        pwd = config.get_str('db', 'pwd')
        port = config.get_int('db', 'port')
        self.mysql = pymysql.connect(host=host, user=user, password=pwd, port=port)  # 1.新建数据库连接
        # self.cursor = self.mysql.cursor()  # 2.新建查询，这种方式查询返回的数据类型是元组
        self.cursor = self.mysql.cursor(pymysql.cursors.DictCursor)#这种方式查询返回的数据是字典


    def fetch_one(self, sql):
        self.cursor.execute(sql)  # 3.执行sql
        self.mysql.commit()
        return self.cursor.fetchone()  # 4.返回查询结果集里最近的一条数据（返回类型取决于创建的cursor）

    def fetch_all(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()  # 返回全部结果（返回类型取决于创建的cursor，如果是元组的话，是元组套元组的形式）

    def close(self):
        self.cursor.close()  # 5.关闭游标
        self.mysql.close()  # 6.关闭数据库连接
