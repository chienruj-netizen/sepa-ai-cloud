from app.core.data_fetcher import fetch_stock_data
from app.core.indicators import calc_indicators
from app.core.ml_predictor import predict
from app.core.tw_stock_list import get_all_stocks
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed


def scan_market(mode="observe"):

    symbols = get_all_stocks()

    temp = []

    # ===== 🚀 STEP 1：並行抓資料 =====
    def fetch_basic(symbol):

        if symbol.startswith("00"):
            return None

        df = fetch_stock_data(symbol)

        if df is None or len(df) < 30:
            return None

        if "close" not in df.columns or "volume" not in df.columns:
            return None

        try:
            close = float(df["close"].iloc[-1])
            prev = float(df["close"].iloc[-2])
            vol = float(df["volume"].iloc[-1])
        except:
            return None

        if prev == 0:
            return None

        change = (close - prev) / prev
        vol_std = df["close"].pct_change().rolling(10).std().iloc[-1]

        return {
            "symbol": symbol,
            "volume": vol,
            "change": change,
            "volatility": vol_std
        }


    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(fetch_basic, s) for s in symbols]

        for f in as_completed(futures):
            res = f.result()
            if res:
                temp.append(res)

    df_rank = pd.DataFrame(temp)

    if len(df_rank) == 0:
        return []

    # ===== 篩選 =====
    df_rank = df_rank.sort_values("volume", ascending=False).head(300)
    df_rank = df_rank.sort_values("change", ascending=False).head(200)
    df_rank = df_rank[df_rank["volatility"] > 0.01]

    symbols = df_rank["symbol"].tolist()

    results = []

    # ===== 🚀 STEP 2：並行 AI 計算 =====
    def analyze_symbol(symbol):

        df = fetch_stock_data(symbol)

        if df is None or len(df) < 60:
            return None

        df = calc_indicators(df)
        row = df.iloc[-1]

        try:
            close = row["close"]
            ma20 = row["ma20"]
            rsi = row["rsi"]
            macd = row["macd"]
            volume = row["volume"]
        except:
            return None

        if ma20 == 0:
            return None

        ma_ratio = close / ma20

        vol_ma20 = df["volume"].rolling(20).mean().iloc[-1]
        if vol_ma20 == 0:
            return None

        vol_ratio = volume / vol_ma20

        momentum_short = df["close"].pct_change().rolling(3).mean().iloc[-1]
        momentum_long = df["close"].pct_change().rolling(6).mean().iloc[-1]

        acceleration = momentum_short - momentum_long

        features = [rsi, macd, ma_ratio, vol_ratio, acceleration]

        prob = predict(features)

        if mode == "observe" and prob < 0.55:
            return None

        if mode == "trade":
            if prob < 0.6 or close < ma20 or vol_ratio < 1.2 or acceleration < 0:
                return None

        return {
            "symbol": symbol,
            "score": round(prob,3),
            "entry": round(close,2),
            "tp": round(close*1.05,2),
            "sl": round(close*0.97,2)
        }


    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(analyze_symbol, s) for s in symbols]

        for f in as_completed(futures):
            res = f.result()
            if res:
                results.append(res)

    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return results[:5]
