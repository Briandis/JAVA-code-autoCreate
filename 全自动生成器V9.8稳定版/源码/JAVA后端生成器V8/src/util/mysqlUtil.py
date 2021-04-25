import pymysql


class MySql:

    def __init__(self, database, cursor=pymysql.cursors.DictCursor,
                 host="127.0.0.1", name="root", password="123456", port=3306):
        self.conn = pymysql.connect(host, name, password, database, port)
        self.cursor_type = cursor

    def execute_select(self, sql_string: str, obj_class) -> list:
        cursor = self.conn.cursor(self.cursor_type)
        cursor.execute(sql_string)
        lists = []
        for i in cursor.fetchall():
            lists.append(self.__create_object(i, obj_class))
        cursor.close()
        return lists

    def execute_dml(self, sql_string: str) -> int:
        cursor = self.conn.cursor(self.cursor_type)
        res = 0
        try:
            res = cursor.execute(sql_string)
            self.conn.commit()
        except:
            self.conn.rollback()
        cursor.close()
        return res

    def close(self):
        self.conn.close()

    def __create_object(self, dict_data: dict, obj_class):
        obj = obj_class()
        for i in dict_data:
            setattr(obj, i, dict_data[i])
        return obj
