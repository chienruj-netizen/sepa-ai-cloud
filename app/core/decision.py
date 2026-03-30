def make_decision(features):

    price = features["price"]
    score = features["score"]
    pattern = features["pattern"]

    if "主升段" in pattern and score > 30:
        action = "🟢 做多"
        tp = round(price * 1.06, 2)
        sl = round(price * 0.97, 2)

    elif "主跌段" in pattern and score > 30:
        action = "🔴 放空"
        tp = round(price * 0.94, 2)
        sl = round(price * 1.03, 2)

    else:
        action = "⚪ 觀察"
        tp = 0
        sl = 0

    reason = f"""
📊 技術：
RSI {features['rsi']} / MACD {features['macd']}

📈 均線：
MA20 {features['ma20']} vs MA60 {features['ma60']}

📰 新聞分數：{features['news']}

🧠 判斷：
{pattern}
"""

    return {
        "action": action,
        "tp": tp,
        "sl": sl,
        "score": score,
        "reason": reason
    }
