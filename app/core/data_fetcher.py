import time
import pandas as pd
from app.core.data_cache import load_from_db, save_to_db, init_db
from app.core.data_fetcher_raw import fetch_finmind, fetch_yahoo

init_db()

_cache = {}
CACHE_TTL = 600


def clean_df(df, symbol):

    # 🔥 MultiIndex 修正
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df.columns.name = None

    # 🔥 全部轉小寫
    df.columns = [str(c).lower() for c in df.columns]

    # 🔥 欄位對齊（超關鍵）
    rename_map = {
        "open": "open",
        "high": "high",
        "low": "low",
        "close": "close",
        "volume": "volume",

        # 常見替代名稱
        "adj close": "close",
        "close_price": "close",
        "收盤價": "close",
        "收盤價(元)": "close",
        "成交股數": "volume",
    }

    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

    # 🔥 確保欄位存在
    required = ["open", "high", "low", "close"]

    for col in required:
        if col not in df.columns:
            raise ValueError(f"缺少欄位: {col} ({symbol})")

    # 🔥 數值化
    for col in ["open", "high", "low", "close", "volume"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df["symbol"] = symbol
    df = df.dropna()

    return df


def get_stock_data(symbol):

    now = time.time()

    if symbol in _cache:
        data, ts = _cache[symbol]
        if now - ts < CACHE_TTL:
            return data

    df = load_from_db(symbol)
    if df is not None and len(df) > 50:
        _cache[symbol] = (df, now)
        return df

    try:
        df = fetch_finmind(symbol)
        if df is not None and len(df) > 0:
            df = clean_df(df, symbol)
            save_to_db(symbol, df)
            _cache[symbol] = (df, now)
            return df
    except Exception as e:
        print(f"⚠️ finmind error: {e}")

    try:
        df = fetch_yahoo(symbol)
        if df is not None and len(df) > 0:
            df = clean_df(df, symbol)
            save_to_db(symbol, df)
            _cache[symbol] = (df, now)
            return df
    except Exception as e:
        print(f"⚠️ yahoo error: {e}")

    return None


def fetch_stock_data(symbol):
    try:
        df = get_stock_data(symbol)

        if df is None or len(df) < 30:
            raise ValueError(f"資料不足: {symbol}")

        return df

    except Exception as e:
        print(f"❌ fetch_stock_data error: {e}")
        return None
