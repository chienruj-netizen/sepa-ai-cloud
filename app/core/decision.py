def make_decision(features):

    pattern = features["pattern"]

    if pattern == "主升段":
        return {
            "action": "🟢 做多",
            "tp": round(features["price"] * 1.05, 2),
            "sl": round(features["price"] * 0.97, 2),
            "reason": "突破＋量能支撐"
        }

    if pattern == "起跌點":
        return {
            "action": "🔴 放空",
            "tp": round(features["price"] * 0.95, 2),
            "sl": round(features["price"] * 1.03, 2),
            "reason": "放量轉弱"
        }

    if pattern == "假突破":
        return {
            "action": "❌ 不做",
            "tp": 0,
            "sl": 0,
            "reason": "量能不足"
        }

    return {
        "action": "⚪ 觀察",
        "tp": 0,
        "sl": 0,
        "reason": "訊號不足"
    }
