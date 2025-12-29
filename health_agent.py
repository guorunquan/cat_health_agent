from core_classes import HealthRecord

class HealthAgent:
    def __init__(self, cat_id):
        self.cat_id = cat_id
        self.record_list = []

    # 感知：获取最新1条单日记录
    def perceive(self):
        self.record_list = HealthRecord.get_history_by_cat_id(self.cat_id)
        return self.record_list is not None and len(self.record_list) >= 1

    # 决策：仅单日检测，汇总所有异常（无体重）
    def decide(self):
        if not self.record_list:
            return "暂无该猫咪的健康记录，无法检测"

        # 只取最新1条单日记录
        latest_record = self.record_list[0]
        # 异常汇总列表
        level1_warnings = []  # 一级预警（紧急）
        level2_warnings = []  # 二级预警（注意）

        # ========== 单日精神状态检测 ==========
        if latest_record["mood"] == "萎靡":
            level1_warnings.append("精神状态萎靡：立即观察是否有呕吐/腹泻，24小时无好转请就医")
        elif latest_record["mood"] == "一般":
            level2_warnings.append("精神状态一般：增加互动，监测饮食和排便")

        # ========== 单日饮食量检测 ==========
        food = latest_record["food"]
        if food < 30:
            level1_warnings.append(f"饮食量极低（{food}g＜30g）：更换适口性好的食物，检查口腔是否有炎症")
        elif food > 200:
            level2_warnings.append(f"饮食量过高（{food}g＞200g）：控制喂食量，避免消化不良")

        # ========== 单日排便检测 ==========
        poop = latest_record["poop"]
        if poop == 0:
            level1_warnings.append("未排便：增加饮水量，喂食少量猫草/化毛膏")
        elif poop >= 5:
            level2_warnings.append(f"排便次数过多（{poop}次≥5次）：检查粪便形态，警惕腹泻")

        # ========== 汇总输出 ==========
        result = ""
        # 一级预警（紧急）
        if level1_warnings:
            result += "🚨 【一级紧急预警】\n" + "\n• ".join(level1_warnings) + "\n\n"
        # 二级预警（注意）
        if level2_warnings:
            result += "⚠️ 【二级注意事项】\n" + "\n• ".join(level2_warnings) + "\n\n"
        # 无异常
        if not level1_warnings and not level2_warnings:
            result += "✅ 【健康评估】单日状态无异常\n建议：保持当前养护节奏，每日固定记录"
        else:
            result += "📌 【总结】请优先处理一级预警问题，持续监测"

        return result

    # 执行：返回检测结果
    def execute(self):
        if self.perceive():
            return self.decide()
        else:
            return "暂无足够的健康记录，无法检测"