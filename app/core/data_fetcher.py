import time
import pandas as pd
from app.core.data_cache import load_from_db, save_to_db, init_db
from app.core.data_fetcher_raw import fetch_finmind, fetch_yahoo

init_db()

_cache = {}
CACHE_TTL = 600


def normalize_columns(df, symbol):

    if df is None or len(df) == 0:
        return None

    # 🔥 MultiIndex 修正（ETF關鍵）
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df.columns = [str(c).lower() for c in df.columns]

    # 🔥 超完整 mapping
    rename_map = {
        "close": "close",
        "adj close": "close",
        "close_price": "close",
        "收盤價": "close",
        "收盤價(元)": "close",

        "open": "open",
        "high": "high",
        "low": "low",
        "volume": "volume",
        "成交股數": "volume"
    }

    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

    # 🔥 如果還沒有 close → 嘗試 fallback
    if "close" not in df.columns:
        if "adj close" in df.columns:
            df["close"] = df["adj close"]
        else:
            print(f"❌ {symbol} 無有效價格欄位 → 跳過")
            return None

    # 數值化
    for col in ["open","high","low","close","volume"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

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
        df = fetch_yahoo(symbol)
        df = normalize_columns(df, symbol)

        if df is not None:
            save_to_db(symbol, df)
            _cache[symbol] = (df, now)
            return df

    except Exception as e:
        print(f"⚠️ yahoo error: {e}")

    return None


def fetch_stock_data(symbol):

    df = get_stock_data(symbol)

    if df is None or len(df) < 30:
        print(f"❌ 資料不足: {symbol}")
        return None

    return df
