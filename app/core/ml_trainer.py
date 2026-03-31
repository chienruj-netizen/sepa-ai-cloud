import pandas as pd
import numpy as np
import joblib
from app.core.data_fetcher import fetch_stock_data
from app.core.indicators import calc_indicators

SYMBOLS = ["2330.TW","2317.TW","1308.TW","2603.TW","2409.TW"]


def build_dataset():

    rows = []

    for symbol in SYMBOLS:

        df = fetch_stock_data(symbol)

        if df is None or len(df) < 80:
            continue

        df = calc_indicators(df)

        for i in range(30, len(df)-5):

            row = df.iloc[i]
            future = df.iloc[i+5]["close"]

            target = 1 if future > row["close"] else 0

            # 🔥 三大特徵
            ma_ratio = row["close"] / row["ma20"] if row["ma20"] else 1

            vol_ma20 = df["volume"].rolling(20).mean().iloc[i]
            vol_ratio = row["volume"] / vol_ma20 if vol_ma20 else 1

            momentum_short = df["close"].pct_change().rolling(3).mean().iloc[i]
            momentum_long = df["close"].pct_change().rolling(6).mean().iloc[i]
            acceleration = momentum_short - momentum_long

            rows.append([
                row["rsi"],
                row["macd"],
                ma_ratio,
                vol_ratio,
                acceleration,
                target
            ])

    df = pd.DataFrame(rows, columns=[
        "rsi","macd","ma_ratio","vol_ratio","acceleration","target"
    ])

    return df


def train():

    from sklearn.ensemble import RandomForestClassifier

    df = build_dataset()

    X = df[["rsi","macd","ma_ratio","vol_ratio","acceleration"]]
    y = df["target"]

    model = RandomForestClassifier(n_estimators=200)
    model.fit(X, y)

    joblib.dump(model, "data/model_v3.pkl")

    print("✅ 模型訓練完成:", X.shape)


if __name__ == "__main__":
    train()
