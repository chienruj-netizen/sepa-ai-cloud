def make_decision(features, trend, score):

    price = features.get("price", 0)
    vol_ratio = features.get("vol_ratio", 1)
    momentum = features.get("momentum", 0)

    # 市場模式
    if trend == "bull":
        mode = "attack"
    elif trend == "bear":
        mode = "short"
    else:
        mode = "defense"

    action = "⚪ 觀察"

    # 做多
    if mode == "attack":
        if score > 0.6 and vol_ratio > 1.2 and momentum > 0:
            action = "🟢 做多"

    # 做空
    elif mode == "short":
        if score < 0.4 and vol_ratio > 1.1 and momentum < 0:
            action = "🔴 做空"

    # 防守
    else:
        if score > 0.7:
            action = "🟡 試單"

    # 風控
    if action == "🟢 做多":
        tp = price * 1.05
        sl = price * 0.97
        rr = (tp - price) / (price - sl)

    elif action == "🔴 做空":
        tp = price * 0.95
        sl = price * 1.03
        rr = (price - tp) / (sl - price)

    else:
        tp = price
        sl = price
        rr = 0

    # 過濾
    if rr < 1.2:
        action = "⚪ 觀察"

    return {
        "action": action,
        "score": round(score * 100, 1),
        "tp": round(tp, 2),
        "sl": round(sl, 2),
        "rr": round(rr, 2),
        "mode": mode
    }
