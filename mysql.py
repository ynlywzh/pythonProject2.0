import pymysql
from flask import config

import app


class MySQL:
    """MySQL数据库操作类"""
    def __init__(self):
        self.conn = None
        self.cur = None


    def connect(self):
        """连接数据库"""
        try:
            self.conn = pymysql.connect(
                host=app.config['DB_HOST'],
                port=app.config['DB_PORT'],
                user=app.config['DB_USER'],
                password=app.config['DB_PASSWORD'],
                db=app.config['DB_NAME']
            )
            self.cur = self.conn.cursor()
        except Exception as e:
            print(f"连接数据库失败: {e}")

    def close(self):
        """关闭数据库"""
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()


    def execute(self, sql, params=None, fetchall=False):
        self.connect()
        self.cur.execute(sql, params)
        if fetchall:
            results = self.cur.fetchall()
            self.close()
            return results
        else:
            self.conn.commit()
            self.close()
            return self.cur.lastrowid
