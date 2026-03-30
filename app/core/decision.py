def make_decision(features):

    price = features["price"]
    score = features["score"]
    pattern = features["pattern"]

    if "起漲" in pattern and score >= 60:
        action = "🟢 佈局（起漲前）"
        tp = round(price * 1.08, 2)
        sl = round(price * 0.96, 2)

    elif "出貨" in pattern:
        action = "🔴 放空"
        tp = round(price * 0.92, 2)
        sl = round(price * 1.04, 2)

    else:
        action = "⚪ 觀察"
        tp = 0
        sl = 0

    reason = f"""
🔥 爆發分析：
量能倍數：{features['vol_ratio']}
法人資金：{features['inst_flow']}
新聞分數：{features['news']}

📊 總評分：{score}
📈 型態：{pattern}
"""

    return {
        "action": action,
        "tp": tp,
        "sl": sl,
        "score": score,
        "reason": reason
    }
