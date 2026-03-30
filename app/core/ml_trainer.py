import pandas as pd
import yfinance as yf
import lightgbm as lgb
import joblib
from app.core.selector import get_candidate_pool


# ========================
# 📥 單股資料
# ========================
def fetch_stock_data(symbol):

    try:
        df = yf.download(symbol, period="1y")

        if df.empty:
            return None

        df["return"] = df["Close"].pct_change(3).shift(-3)

        # 🔥 技術特徵
        df["rsi"] = df["Close"].pct_change().rolling(14).mean()
        df["volume_ratio"] = df["Volume"] / df["Volume"].rolling(20).mean()
        df["ma20"] = df["Close"].rolling(20).mean()

        # 🔥 V7特徵
        df["volatility"] = abs(df["rsi"] - df["rsi"].rolling(20).mean())
        df["institution"] = 0  # 之後可接 FinMind

        return df

    except Exception as e:
        print(f"❌ {symbol} error:", e)
        return None


# ========================
# 📊 建立全市場資料集
# ========================
def build_dataset():

    symbols = get_candidate_pool()

    all_data = []

    for i, symbol in enumerate(symbols[:100]):  # 🔥 控制訓練量

        print(f"📊 [{i+1}/100] {symbol}")

        df = fetch_stock_data(symbol)

        if df is not None:
            all_data.append(df)

    if not all_data:
        raise ValueError("❌ 無法取得任何股票資料")

    df_all = pd.concat(all_data)

    df_all = df_all.dropna()

    X = df_all[[
        "rsi",
        "volume_ratio",
        "ma20",
        "volatility",
        "institution"
    ]]

    y = df_all["return"]

    return X, y


# ========================
# 🔥 訓練模型（V7）
# ========================
def train_models():

    print("🚀 開始全市場模型訓練")

    X, y = build_dataset()

    print(f"📊 訓練資料筆數: {len(X)}")

    # 📈 報酬模型
    model_return = lgb.LGBMRegressor(
        n_estimators=300,
        learning_rate=0.05
    )
    model_return.fit(X, y)

    joblib.dump(model_return, "data/model_return.pkl")

    # 📊 波動模型
    y_vol = abs(y)

    model_vol = lgb.LGBMRegressor(
        n_estimators=300,
        learning_rate=0.05
    )
    model_vol.fit(X, y_vol)

    joblib.dump(model_vol, "data/model_vol.pkl")

    print("✅ 全市場模型訓練完成（V7）")
