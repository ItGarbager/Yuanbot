import sqlite3


class LiteDb:
    """
    simpleToolSql for sqlite3
    简单数据库工具类
    编写这个类主要是为了封装sqlite，继承此类复用方法
    """

    _instance = None

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, filename="bot"):
        """
        初始化数据库，默认文件名 bot.db
        filename：文件名
        """
        self.filename = filename + ".db"
        self.db = sqlite3.connect(self.filename)
        self.c = self.db.cursor()

    def create_table(self, sql):
        """
        example：'create table userinfo(name text, email text)'
        :return: result=[1,None]
        """
        self.c.execute(sql)
        self.db.commit()
        return None

    def drop_table(self, sql):
        """
        example: 'drop table userinfo'
        :param sql:
        :return: result=[1,None]
        """
        self.c.execute(sql)
        self.db.commit()
        return None

    def close(self):
        """
        关闭数据库
        """
        self.c.close()
        self.db.close()

    def execute(self, sql, param=None):
        """
        执行数据库的增、删、改
        sql：sql语句
        param：数据，可以是list或tuple，亦可是None
        retutn：成功返回True
        """
        try:
            if param is None:
                self.c.execute(sql)
            else:
                if type(param) is list:
                    self.c.executemany(sql, param)
                else:
                    self.c.execute(sql, param)
            count = self.db.total_changes
            self.db.commit()
        except Exception as e:
            print(e)
            return False, e
        if count > 0:
            return True
        else:
            return False

    def query(self, sql, param=None):
        """
        查询语句
        sql：sql语句
        param：参数,可为None
        retutn：成功返回True
        """
        if param is None:
            self.c.execute(sql)
        else:
            self.c.execute(sql, param)
        return self.c.fetchall()
