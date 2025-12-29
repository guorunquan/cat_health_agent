import sys
from PyQt5.QtWidgets import *
from core_classes import Cat, HealthRecord
from health_agent import HealthAgent

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("智能猫咪健康监护助手")
        self.setGeometry(100, 100, 500, 450)

        # 布局
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # 按钮（新增「修改猫咪信息」按钮）
        self.btn_add_cat = QPushButton("添加猫咪信息")
        self.btn_edit_cat = QPushButton("修改猫咪信息")  # 新增按钮
        self.btn_add_record = QPushButton("添加单日健康记录")
        self.btn_check = QPushButton("单日健康检测")
        self.txt_result = QTextEdit()
        self.txt_result.setPlaceholderText("检测结果会显示在这里...")

        # 绑定事件（新增修改猫咪的事件绑定）
        self.btn_add_cat.clicked.connect(self.add_cat)
        self.btn_edit_cat.clicked.connect(self.edit_cat)  # 新增绑定
        self.btn_add_record.clicked.connect(self.add_record)
        self.btn_check.clicked.connect(self.check_health)

        # 添加组件（新增按钮加到布局）
        layout.addWidget(self.btn_add_cat)
        layout.addWidget(self.btn_edit_cat)
        layout.addWidget(self.btn_add_record)
        layout.addWidget(self.btn_check)
        layout.addWidget(self.txt_result)

    # 添加猫咪
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

    # 新增：修改猫咪信息功能
    def edit_cat(self):
        # 先获取所有猫咪列表
        cats = Cat.get_all_cats()
        if not cats:
            QMessageBox.warning(self, "提示", "暂无猫咪信息，请先添加！")
            return

        # 选择要修改的猫咪
        cat_options = [f"{c['name']} (ID:{c['cat_id']})" for c in cats]
        cat_choice, ok1 = QInputDialog.getItem(self, "修改猫咪", "选择要修改的猫咪：", cat_options)
        if not ok1:
            return

        # 提取猫咪ID并获取当前信息
        cat_id = int(cat_choice.split("ID:")[1].replace(")", ""))
        current_cat = Cat.get_cat_by_id(cat_id)
        if not current_cat:
            QMessageBox.warning(self, "错误", "未找到该猫咪信息！")
            return

        # 弹出输入框（默认填充当前信息）
        name, ok2 = QInputDialog.getText(self, "修改猫咪", "新名字：", text=current_cat["name"])
        breed, ok3 = QInputDialog.getText(self, "修改猫咪", "新品种：", text=current_cat["breed"])
        age, ok4 = QInputDialog.getInt(self, "修改猫咪", "新年龄（岁）：", value=current_cat["age"], min=0)

        # 保存修改
        if ok2 and ok3 and ok4:
            cat = Cat(cat_id=cat_id, name=name, breed=breed, age=age)
            if cat.update():
                QMessageBox.information(self, "成功", "猫咪信息修改成功！")
            else:
                QMessageBox.warning(self, "失败", "修改失败！")

    # 添加单日健康记录（无体重）
    def add_record(self):
        cats = Cat.get_all_cats()
        if not cats:
            QMessageBox.warning(self, "提示", "先添加猫咪！")
            return

        # 选猫咪
        cat_options = [f"{c['name']} (ID:{c['cat_id']})" for c in cats]
        cat_choice, ok1 = QInputDialog.getItem(self, "选猫咪", "选择记录的猫咪：", cat_options)
        if not ok1:
            return
        cat_id = int(cat_choice.split("ID:")[1].replace(")", ""))

        # 单日记录输入（无体重）
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

    # 单日健康检测
    def check_health(self):
        cats = Cat.get_all_cats()
        if not cats:
            QMessageBox.warning(self, "提示", "先添加猫咪！")
            return

        # 选猫咪
        cat_options = [f"{c['name']} (ID:{c['cat_id']})" for c in cats]
        cat_choice, ok = QInputDialog.getItem(self, "选猫咪", "检测的猫咪：", cat_options)
        if ok:
            cat_id = int(cat_choice.split("ID:")[1].replace(")", ""))
            agent = HealthAgent(cat_id)
            result = agent.execute()
            self.txt_result.setText(result)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())