from app.core.selector import pick_candidates
from app.core.decision import make_decision
from app.core.data_fetcher import get_stock_data


def run_pipeline():

    candidates = pick_candidates()

    # 🔥 限制數量（避免卡）
    candidates = candidates[:3]

    trades = []

    for c in candidates:

        d = make_decision(c, "bull", c["prob"])

        # 🔥 重點：只排除 HOLD
        if d["action"] == "HOLD":
            continue

        df = get_stock_data(c["symbol"])

        if df is None or len(df) == 0:
            continue

        price = float(df["close"].iloc[-1])

        trades.append({
            "symbol": c["symbol"],
            "prob": c["prob"],
            "side": d["side"],  # 🔥 用 decision 的
            "price": price
        })

    return trades
