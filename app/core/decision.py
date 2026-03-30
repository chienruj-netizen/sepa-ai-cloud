from app.core.backtest import log_trade
from app.core.adaptive import get_strategy_mode
from app.core.reversal import detect_reversal
from app.core.ai_optimizer import load_best


def make_decision(features, trend, score):

    price = float(features.get("price", 0))
    vol_ratio = float(features.get("vol_ratio", 1))
    momentum = float(features.get("momentum", 0))

    # =====================
    # 🧠 AI自動調參（V3）
    # =====================
    strategy = get_strategy_mode()
    mode = strategy["mode"]

    # =====================
    # 🤖 自動最佳參數（V5）
    # =====================
    config = load_best()
    threshold = config.get("threshold", 0.6)
    vol_req = config.get("vol_ratio", 1.2)

    action = "⚪ 觀察"

    # =====================
    # 💣 起跌點雷達（最高優先）
    # =====================
    if detect_reversal(features):
        tp = price * 0.95
        sl = price * 1.03
        rr = (price - tp) / (sl - price)

        return {
            "action": "🔴 做空",
            "score": round(score * 100, 1),
            "tp": round(tp, 2),
            "sl": round(sl, 2),
            "rr": round(rr, 2),
            "mode": "reversal",
            "reason": "偵測到起跌訊號（RSI/MACD/動能轉弱）"
        }

    # =====================
    # 🚀 做多策略
    # =====================
    if mode == "attack":
        if score > threshold and vol_ratio > vol_req and momentum > 0:
            action = "🟢 做多"

    # =====================
    # 🔴 做空策略
    # =====================
    elif mode == "defense":
        if score < (1 - threshold) and momentum < 0:
            action = "🔴 做空"

    # =====================
    # 🟡 試單
    # =====================
    else:
        if score > 0.65:
            action = "🟡 試單"

    # =====================
    # 🛡 風控
    # =====================
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

    # =====================
    # 🚫 RR過濾
    # =====================
    if rr < 1.2:
        action = "⚪ 觀察"

    # =====================
    # 📊 記錄交易（關鍵）
    # =====================
    if action in ["🟢 做多", "🔴 做空"]:
        try:
            log_trade(
                features.get("symbol"),
                action,
                price,
                tp,
                sl
            )
        except:
            pass

    # =====================
    # 📦 回傳
    # =====================
    return {
        "action": action,
        "score": round(score * 100, 1),
        "tp": round(tp, 2),
        "sl": round(sl, 2),
        "rr": round(rr, 2),
        "mode": mode,
        "reason": f"score={round(score,2)}, vol={round(vol_ratio,2)}, momentum={round(momentum,2)}"
    }
