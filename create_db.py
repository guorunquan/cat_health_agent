import sqlite3
import os

# 删除旧数据库文件
db_path = "db/cat_health.db"
if os.path.exists(db_path):
    os.remove(db_path)

# 创建db文件夹
if not os.path.exists("db"):
    os.makedirs("db")

# 连接数据库并创建表（完全去掉SQL内的注释）
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 创建cat表（无注释）
cursor.execute('''
CREATE TABLE IF NOT EXISTS cat (
    cat_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    breed TEXT NOT NULL,
    age INTEGER NOT NULL
)
''')

# 创建health_record表（无注释）
cursor.execute('''
CREATE TABLE IF NOT EXISTS health_record (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    cat_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    food REAL NOT NULL,
    poop INTEGER NOT NULL,
    mood TEXT NOT NULL
)
''')

# 提交并关闭
conn.commit()
conn.close()
print("数据库创建成功！")