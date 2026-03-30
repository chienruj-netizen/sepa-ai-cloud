from app.core.backtest import log_trade
from app.core.adaptive import get_strategy_mode
from app.core.reversal import detect_reversal
from app.core.ai_optimizer import load_best
from app.core.gpt_decision import gpt_decide


def make_decision(features, trend, score):

    price = float(features.get("price", 0))
    vol_ratio = float(features.get("vol_ratio", 1))
    momentum = float(features.get("momentum", 0))

    # =====================
    # 🧠 策略模式
    # =====================
    strategy = get_strategy_mode()
    mode = strategy["mode"]

    # =====================
    # 🤖 最佳參數
    # =====================
    config = load_best()
    threshold = config.get("threshold", 0.6)
    vol_req = config.get("vol_ratio", 1.2)

    # =====================
    # 💣 起跌點（最高優先）
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
            "reason": "起跌點訊號（優先）"
        }

    # =====================
    # 🟢 策略初篩（關鍵）
    # =====================
    strategy_signal = "⚪ 觀察"

    if mode == "attack":
        if score > threshold and vol_ratio > vol_req and momentum > 0:
            strategy_signal = "🟢 做多"

    elif mode == "defense":
        if score < (1 - threshold) and momentum < 0:
            strategy_signal = "🔴 做空"

    else:
        if score > 0.65:
            strategy_signal = "🟡 試單"

    # 👉 如果策略都不過 → 直接跳過（省 GPT 成本）
    if strategy_signal == "⚪ 觀察":
        return {
            "action": "⚪ 觀察",
            "score": round(score * 100, 1),
            "tp": price,
            "sl": price,
            "rr": 0,
            "mode": "filter",
            "reason": "策略未通過"
        }

    # =====================
    # 🤖 GPT最終決策（核心🔥）
    # =====================
    gpt = gpt_decide(features, trend)

    action_map = {
        "做多": "🟢 做多",
        "做空": "🔴 做空",
        "觀察": "⚪ 觀察"
    }

    action = action_map.get(gpt.get("action"), strategy_signal)

    tp = float(gpt.get("tp", price))
    sl = float(gpt.get("sl", price))

    # =====================
    # 🛡 風控
    # =====================
    if action == "🟢 做多":
        rr = (tp - price) / (price - sl) if price != sl else 0

    elif action == "🔴 做空":
        rr = (price - tp) / (sl - price) if price != sl else 0

    else:
        rr = 0

    # =====================
    # 🚫 過濾低品質
    # =====================
    if rr < 1.2 or gpt.get("confidence", 0) < 0.55:
        action = "⚪ 觀察"

    # =====================
    # 📊 記錄交易
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
        "mode": "hybrid",
        "reason": gpt.get("reason", "策略+AI融合")
    }
