
def make_decision(symbol, trend=None, score=None):

    if score is None:
        score = 0.5

    # 🔥 分級（關鍵）
    if score >= 0.75:
        action = "STRONG_BUY"
        position = 1.0
    elif score >= 0.65:
        action = "BUY"
        position = 0.5
    elif score >= 0.5:
        action = "HOLD"
        position = 0
    else:
        action = "SELL"
        position = 0

    # 🔥 交易策略
    entry = "next_open" if position > 0 else None
    tp = "+5%" if position > 0 else None
    sl = "-3%" if position > 0 else None

    decision = {
        "symbol": symbol,
        "action": action,
        "score": round(score, 3),
        "position": position,
        "entry": entry,
        "tp": tp,
        "sl": sl
    }

    print(f"📌 {symbol} → {action} (score={score})")

    return decision
