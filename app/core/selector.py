import requests
import pandas as pd
import os

# ========================
# 🔥 TWSE 全市場（上市）
# ========================
def fetch_twse_list():
    try:
        url = "https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL"
        res = requests.get(url, timeout=5)
        df = pd.DataFrame(res.json())

        df["close"] = pd.to_numeric(df["ClosingPrice"], errors="coerce")
        df["volume"] = pd.to_numeric(df["TradeVolume"], errors="coerce")

        return df[["Code", "close", "volume"]]

    except Exception as e:
        print("TWSE list error:", e)
        return None


# ========================
# 🔥 FinMind（備援）
# ========================
def fetch_finmind_list():
    token = os.getenv("FINMIND_TOKEN")

    if not token:
        return None

    try:
        url = "https://api.finmindtrade.com/api/v4/data"
        params = {
            "dataset": "TaiwanStockInfo",
            "token": token
        }

        res = requests.get(url, params=params, timeout=5)
        data = res.json()["data"]

        df = pd.DataFrame(data)

        # 過濾上市股票
        df = df[df["industry_category"] != None]

        return df[["stock_id"]]

    except Exception as e:
        print("FinMind list error:", e)
        return None


# ========================
# 🔥 核心：全市場股票池
# ========================
def get_candidate_pool():

    # 1️⃣ TWSE 優先
    df = fetch_twse_list()

    symbols = []

    if df is not None:

        # 🔥 基本過濾（避免垃圾股）
        df = df[
            (df["close"] > 20) &        # 價格太低不要
            (df["volume"] > 1000)      # 成交量太低不要
        ]

        symbols = df["Code"].tolist()

    else:
        # 2️⃣ FinMind fallback
        fm = fetch_finmind_list()
        if fm is not None:
            symbols = fm["stock_id"].tolist()

    # 🔥 加 .TW
    symbols = [f"{s}.TW" for s in symbols]

    # 🔥 限制數量（避免爆 API）
    return symbols[:200]
