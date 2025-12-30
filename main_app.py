import sys
from PyQt5.QtWidgets import *
from core_classes import Cat, HealthRecord
from health_agent import HealthAgent

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("智能猫咪健康监护助手")
        self.setGeometry(100, 100, 600, 500)  # 放大窗口，适配查询结果

        # 布局
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # 按钮（新增「查询健康信息」按钮）
        self.btn_add_cat = QPushButton("添加猫咪信息")
        self.btn_edit_cat = QPushButton("修改猫咪信息")
        self.btn_add_record = QPushButton("添加单日健康记录")
        self.btn_check = QPushButton("单日健康检测")
        self.btn_query = QPushButton("查询猫咪健康信息")  # 新增按钮
        self.txt_result = QTextEdit()
        self.txt_result.setPlaceholderText("操作结果/查询结果会显示在这里...")

        # 绑定事件（新增查询事件）
        self.btn_add_cat.clicked.connect(self.add_cat)
        self.btn_edit_cat.clicked.connect(self.edit_cat)
        self.btn_add_record.clicked.connect(self.add_record)
        self.btn_check.clicked.connect(self.check_health)
        self.btn_query.clicked.connect(self.query_health_info)  # 新增绑定

        # 添加组件（新增按钮加到布局）
        layout.addWidget(self.btn_add_cat)
        layout.addWidget(self.btn_edit_cat)
        layout.addWidget(self.btn_add_record)
        layout.addWidget(self.btn_check)
        layout.addWidget(self.btn_query)
        layout.addWidget(self.txt_result)

    # 原有功能（add_cat/edit_cat/add_record/check_health）保持不变 ↓
    def add_cat(self):
        name, ok1 = QInputDialog.getText(self, "添加猫咪", "名字：")
        breed, ok2 = QInputDialog.getText(self, "添加猫咪", "品种：")
        age, ok3 = QInputDialog.getInt(self, "添加猫咪", "年龄（岁）：", min=0)
        if ok1 and ok2 and ok3:
            cat = Cat(name=name, breed=breed, age=age)
            if cat.save():
                QMessageBox.information(self, "成功", "猫咪添加成功！")
            else:
                QMessageBox.warning(self, "失败", "添加失败！")

    def edit_cat(self):
        cats = Cat.get_all_cats()
        if not cats:
            QMessageBox.warning(self, "提示", "暂无猫咪信息，请先添加！")
            return
        cat_options = [f"{c['name']} (ID:{c['cat_id']})" for c in cats]
        cat_choice, ok1 = QInputDialog.getItem(self, "修改猫咪", "选择要修改的猫咪：", cat_options)
        if not ok1:
            return
        cat_id = int(cat_choice.split("ID:")[1].replace(")", ""))
        current_cat = Cat.get_cat_by_id(cat_id)
        if not current_cat:
            QMessageBox.warning(self, "错误", "未找到该猫咪信息！")
            return
        name, ok2 = QInputDialog.getText(self, "修改猫咪", "新名字：", text=current_cat["name"])
        breed, ok3 = QInputDialog.getText(self, "修改猫咪", "新品种：", text=current_cat["breed"])
        age, ok4 = QInputDialog.getInt(self, "修改猫咪", "新年龄（岁）：", value=current_cat["age"], min=0)
        if ok2 and ok3 and ok4:
            cat = Cat(cat_id=cat_id, name=name, breed=breed, age=age)
            if cat.update():
                QMessageBox.information(self, "成功", "猫咪信息修改成功！")
            else:
                QMessageBox.warning(self, "失败", "修改失败！")

    def add_record(self):
        cats = Cat.get_all_cats()
        if not cats:
            QMessageBox.warning(self, "提示", "先添加猫咪！")
            return
        cat_options = [f"{c['name']} (ID:{c['cat_id']})" for c in cats]
        cat_choice, ok1 = QInputDialog.getItem(self, "选猫咪", "选择记录的猫咪：", cat_options)
        if not ok1:
            return
        cat_id = int(cat_choice.split("ID:")[1].replace(")", ""))
        date, ok2 = QInputDialog.getText(self, "单日记录", "日期（2025-10-01）：")
        food, ok3 = QInputDialog.getDouble(self, "单日记录", "饮食量（g）：", min=0.0)
        poop, ok4 = QInputDialog.getInt(self, "单日记录", "排便次数：", min=0)
        mood, ok5 = QInputDialog.getItem(self, "单日记录", "精神状态：", ["活跃", "一般", "萎靡"])
        if ok2 and ok3 and ok4 and ok5:
            record = HealthRecord(cat_id=cat_id, date=date, food=food, poop=poop, mood=mood)
            if record.save():
                QMessageBox.information(self, "成功", "单日记录添加成功！")
            else:
                QMessageBox.warning(self, "失败", "添加失败！")

    def check_health(self):
        cats = Cat.get_all_cats()
        if not cats:
            QMessageBox.warning(self, "提示", "先添加猫咪！")
            return
        cat_options = [f"{c['name']} (ID:{c['cat_id']})" for c in cats]
        cat_choice, ok = QInputDialog.getItem(self, "选猫咪", "检测的猫咪：", cat_options)
        if ok:
            cat_id = int(cat_choice.split("ID:")[1].replace(")", ""))
            agent = HealthAgent(cat_id)
            result = agent.execute()
            self.txt_result.setText(result)

    # 新增：查询猫咪健康信息功能 ↓
    def query_health_info(self):
        # 1. 选择要查询的猫咪
        cats = Cat.get_all_cats()
        if not cats:
            QMessageBox.warning(self, "提示", "暂无猫咪信息，请先添加！")
            return
        cat_options = [f"{c['name']} (ID:{c['cat_id']})" for c in cats]
        cat_choice, ok1 = QInputDialog.getItem(self, "查询健康信息", "选择要查询的猫咪：", cat_options)
        if not ok1:
            return
        cat_id = int(cat_choice.split("ID:")[1].replace(")", ""))
        cat_info = Cat.get_cat_by_id(cat_id)

        # 2. 获取该猫咪的所有健康记录
        records = HealthRecord.get_history_by_cat_id(cat_id)
        if not records:
            self.txt_result.setText(f"🐱 猫咪信息：{cat_info['name']}（品种：{cat_info['breed']}，年龄：{cat_info['age']}岁）\n\n⚠️ 暂无健康记录！")
            return

        # 3. 拼接查询结果（日期+记录详情+检测结果）
        result = f"🐱 猫咪信息：{cat_info['name']}（品种：{cat_info['breed']}，年龄：{cat_info['age']}岁）\n\n"
        result += "📜 健康记录汇总（按日期倒序）：\n"
        result += "----------------------------------------\n"

        # 遍历每条记录，生成对应检测结果
        for idx, record in enumerate(records, 1):
            # 构造单条记录的临时智能体，生成检测结果
            temp_agent = HealthAgent(cat_id)
            temp_agent.record_list = [record]  # 仅传入当前条记录
            detect_result = temp_agent.decide()

            # 拼接单条记录详情
            result += f"【第{idx}条记录】\n"
            result += f"日期：{record['date']}\n"
            result += f"健康记录：饮食{record['food']}g | 排便{record['poop']}次 | 精神状态{record['mood']}\n"
            result += f"检测结果：{detect_result}\n"
            result += "----------------------------------------\n"

        # 4. 显示最终结果
        self.txt_result.setText(result)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
