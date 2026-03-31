from app.core.selector import scan_market
from app.core.decision import make_decision
from app.core.data_fetcher import get_stock_data
from app.core.portfolio import open_position

def run_pipeline():

    candidates = scan_market(mode="trade")

    trades = []

    for c in candidates:

        decision = make_decision(c, "bull", c["score"])

        if decision["action"] == "HOLD":
            continue

        df = get_stock_data(c["symbol"])

        # 🔥 關鍵防呆（close錯誤終結）
        if df is None or "close" not in df.columns:
            continue

        price = float(df["close"].iloc[-1])

        open_position(c["symbol"], price, decision["action"])

        trades.append({
            "symbol": c["symbol"],
            "price": price,
            "prob": c["score"],
            "action": decision["action"]
        })

    return trades
