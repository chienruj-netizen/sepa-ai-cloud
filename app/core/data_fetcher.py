import time
import pandas as pd
from app.core.data_cache import load_from_db, save_to_db, init_db
from app.core.data_fetcher_raw import fetch_finmind, fetch_yahoo

init_db()

# 🔥 記憶體快取（關鍵）
_cache = {}
CACHE_TTL = 600  # 10分鐘


def clean_df(df, symbol):
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df.columns.name = None

    df = df.rename(columns={
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "volume"
    })

    for col in ["open", "high", "low", "close", "volume"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df["symbol"] = symbol
    df = df.dropna()

    return df


def get_stock_data(symbol):

    now = time.time()

    # 🔥 1️⃣ 記憶體快取（最快）
    if symbol in _cache:
        data, ts = _cache[symbol]
        if now - ts < CACHE_TTL:
            return data

    # 🔥 2️⃣ DB 快取
    df = load_from_db(symbol)
    if df is not None and len(df) > 50:
        _cache[symbol] = (df, now)
        return df

    # 🔥 3️⃣ FinMind（優先）
    try:
        df = fetch_finmind(symbol)
        if df is not None and len(df) > 0:
            df = clean_df(df, symbol)
            save_to_db(symbol, df)
            _cache[symbol] = (df, now)
            return df
    except:
        pass

    # 🔥 4️⃣ Yahoo（備援）
    try:
        df = fetch_yahoo(symbol)
        if df is not None and len(df) > 0:
            df = clean_df(df, symbol)
            save_to_db(symbol, df)
            _cache[symbol] = (df, now)
            return df
    except:
        pass

    return None


def fetch_stock_data(symbol):
    try:
        df = get_stock_data(symbol)

        if df is None or len(df) < 30:
            raise ValueError(f"資料不足: {symbol}")

        return df

    except Exception as e:
        print(f"⚠️ fetch_stock_data error: {e}")
        return None
