from db_connector import Database

class Cat:
    def __init__(self, cat_id=None, name="", breed="", age=0):
        self.cat_id = cat_id
        self.name = name
        self.breed = breed
        self.age = age
        self.db = Database()

    # 保存新猫咪
    def save(self):
        sql = "INSERT INTO cat (name, breed, age) VALUES (?, ?, ?)"
        data = (self.name, self.breed, self.age)
        return self.db.insert(sql, data)

    # 修改猫咪信息（新增核心功能）
    def update(self):
        if not self.cat_id:
            return False
        sql = "UPDATE cat SET name=?, breed=?, age=? WHERE cat_id=?"
        data = (self.name, self.breed, self.age, self.cat_id)
        return self.db.insert(sql, data)

    # 获取所有猫咪
    @staticmethod
    def get_all_cats():
        db = Database()
        sql = "SELECT * FROM cat"
        return db.query(sql)

    # 根据ID获取单只猫咪信息（用于修改）
    @staticmethod
    def get_cat_by_id(cat_id):
        db = Database()
        sql = "SELECT * FROM cat WHERE cat_id=?"
        result = db.query(sql, (cat_id,))
        if result:
            return result[0]
        return None

class HealthRecord:
    def __init__(self, record_id=None, cat_id=0, date="", food=0.0, poop=0, mood=""):
        self.record_id = record_id
        self.cat_id = cat_id
        self.date = date
        self.food = food
        self.poop = poop
        self.mood = mood
        self.db = Database()

    # 保存单日健康记录
    def save(self):
        sql = "INSERT INTO health_record (cat_id, date, food, poop, mood) VALUES (?, ?, ?, ?, ?)"
        data = (self.cat_id, self.date, self.food, self.poop, self.mood)
        return self.db.insert(sql, data)

    # 根据猫咪ID获取记录
    @staticmethod
    def get_history_by_cat_id(cat_id):
        db = Database()
        sql = "SELECT * FROM health_record WHERE cat_id = ? ORDER BY date DESC"
        return db.query(sql, (cat_id,))