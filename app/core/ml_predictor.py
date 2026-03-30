import pandas as pd
from app.core.data_fetcher import fetch_stock_data
from app.core.ml_trainer import train_models


# 🔥 共用標準化（跟 trainer 一樣）
def normalize_columns(df):
    df.columns = [str(c).lower() for c in df.columns]

    new_cols = {}
    for col in df.columns:
        if "open" in col:
            new_cols[col] = "open"
        elif "high" in col:
            new_cols[col] = "high"
        elif "low" in col:
            new_cols[col] = "low"
        elif "close" in col:
            new_cols[col] = "close"
        elif "volume" in col:
            new_cols[col] = "volume"

    df = df.rename(columns=new_cols)
    return df


# 🔥 模型（先簡單）
model = train_models()


def build_features(df):
    df = normalize_columns(df)

    required = ["open", "high", "low", "close", "volume"]
    for col in required:
        if col not in df.columns:
            raise ValueError(f"缺少欄位: {col}, 目前: {df.columns}")

    df["ma5"] = df["close"].rolling(5).mean()
    df["ma20"] = df["close"].rolling(20).mean()
    df["return"] = df["close"].pct_change()

    df = df.dropna()
    return df


def predict_stock(symbol):
    df = fetch_stock_data(symbol)

    if df is None or len(df) < 50:
        return None

    df = build_features(df)

    latest = df.iloc[-1]

    X = [[
        latest["open"],
        latest["high"],
        latest["low"],
        latest["close"],
        latest["volume"],
        latest["ma5"],
        latest["ma20"]
    ]]

    prob = model.predict_proba(X)[0][1]

    return {
        "symbol": symbol,
        "prob": round(prob, 3),
        "price": latest["close"]
    }


if __name__ == "__main__":
    print("🚀 預測中...")
    result = predict_stock("2330.TW")
    print(result)
