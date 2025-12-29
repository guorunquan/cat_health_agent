import sqlite3
import os

class Database:
    def __init__(self):
        # 数据库路径：指向你刚才建的db文件夹里的cat_health.db
        self.db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "db/cat_health.db")
        self.conn = None

    # 连接数据库
    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            return self.conn
        except Exception as e:
            print(f"数据库连接失败：{e}")
            return None

    # 插入数据（添加猫咪/健康记录）
    def insert(self, sql, data):
        conn = self.connect()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql, data)
                conn.commit()
                return True
            except Exception as e:
                print(f"插入数据失败：{e}")
                conn.rollback()
                return False
            finally:
                cursor.close()
                conn.close()

    # 查询数据（获取猫咪/历史记录）
    def query(self, sql, data=None):
        conn = self.connect()
        if conn:
            cursor = conn.cursor()
            try:
                if data:
                    cursor.execute(sql, data)
                else:
                    cursor.execute(sql)
                result = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                return [dict(zip(columns, row)) for row in result]
            except Exception as e:
                print(f"查询数据失败：{e}")
                return None
            finally:
                cursor.close()
                conn.close()