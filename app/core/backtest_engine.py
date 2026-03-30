import yfinance as yf
import pandas as pd

from app.core.analysis import analyze_stock
from app.core.decision import make_decision
from app.core.radar import detect_trend


def run_backtest(symbol="2330.TW"):

    df = yf.download(symbol, period="6mo", interval="1d")

    results = []

    for i in range(60, len(df) - 3):

        sub_df = df.iloc[:i].copy()

        # 模擬 features（簡化版）
        try:
            features = analyze_stock({"symbol": symbol})
            if not features:
                continue

            trend = detect_trend(features)
            score = features["score"]

            decision = make_decision(features, trend, score)

            action = decision["action"]

            if action not in ["🟢 做多", "🔴 做空"]:
                continue

            entry = float(df["Close"].iloc[i])
            exit_price = float(df["Close"].iloc[i + 3])

            # 多單
            if action == "🟢 做多":
                ret = (exit_price - entry) / entry

            # 空單
            else:
                ret = (entry - exit_price) / entry

            results.append({
                "action": action,
                "entry": entry,
                "exit": exit_price,
                "return": ret
            })

        except:
            continue

    return pd.DataFrame(results)
