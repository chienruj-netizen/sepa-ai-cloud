import pandas as pd
from app.core.data_fetcher import fetch_stock_data


def normalize_columns(df):
    # 🔥 統一欄位（不管來源）
    df.columns = [str(c).lower() for c in df.columns]

    mapping = {
        "open": "open",
        "high": "high",
        "low": "low",
        "close": "close",
        "volume": "volume"
    }

    # 找相似欄位
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


def build_dataset(symbol="2330.TW"):
    df = fetch_stock_data(symbol)

    if df is None or len(df) < 50:
        raise ValueError("資料不足")

    # 🔥 強制標準化
    df = normalize_columns(df)

    required = ["open", "high", "low", "close", "volume"]

    for col in required:
        if col not in df.columns:
            raise ValueError(f"缺少欄位: {col}，目前欄位: {df.columns}")

    # 🔥 特徵工程
    df["return"] = df["close"].pct_change()
    df["ma5"] = df["close"].rolling(5).mean()
    df["ma20"] = df["close"].rolling(20).mean()

    df = df.dropna()

    X = df[["open", "high", "low", "close", "volume", "ma5", "ma20"]]
    y = (df["return"] > 0).astype(int)

    return X, y


def train_models():
    X, y = build_dataset()

    print("📊 Dataset:", X.shape)
    print("🎯 Label:", y.shape)

    from sklearn.ensemble import RandomForestClassifier

    model = RandomForestClassifier()
    model.fit(X, y)

    print("✅ Model training complete")

    return model


if __name__ == "__main__":
    print("🚀 開始訓練模型...")
    model = train_models()
