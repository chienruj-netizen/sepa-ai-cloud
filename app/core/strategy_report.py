from app.core.market_regime import get_market_regime
from app.core.ai_optimizer import CONFIG


def build_trade_plan(candidate, decision):

    price = candidate.get("price", 0)
    prob = candidate.get("prob", 0)

    tp = CONFIG["tp"]
    sl = CONFIG["sl"]

    # 🔥 做多
    if decision["action"] == "BUY":
        tp_price = price * (1 + tp)
        sl_price = price * (1 + sl)

    # 🔥 做空
    else:
        tp_price = price * (1 - tp)
        sl_price = price * (1 - sl)

    return {
        "symbol": candidate["symbol"],
        "action": decision["action"],
        "price": round(price, 2),
        "tp": round(tp_price, 2),
        "sl": round(sl_price, 2),
        "prob": round(prob, 2)
    }


def format_report(trades):

    market = get_market_regime()

    msg = f"📊 今日策略（AI）\n\n🌍 市場：{market}\n\n"

    for t in trades:

        icon = "🟢" if t["action"] == "BUY" else "🔴"

        msg += f"{icon} {t['symbol']}\n"
        msg += f"AI：{t['prob']}\n"
        msg += f"進場：{t['price']}\n"
        msg += f"TP：{t['tp']}\n"
        msg += f"SL：{t['sl']}\n\n"

    return msg
