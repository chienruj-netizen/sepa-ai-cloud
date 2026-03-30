import pandas as pd
from app.core.data_cache import load_from_db, save_to_db, init_db
from app.core.data_fetcher_raw import fetch_finmind, fetch_yahoo
from app.core.cache import get_cache, set_cache
from app.core.redis_cache import get_redis, set_redis
from app.core.rate_limiter import rate_limit
from app.core.retry import retry

init_db()


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


def fetch_with_retry(func):
    return retry(lambda: func(), retries=3, delay=1)


def get_stock_data(symbol, tf="1d"):
    key = f"{symbol}_{tf}"

    # 🔥 ① Memory Cache
    data = get_cache(key, tf)
    if data is not None:
        return data

    # 🔥 ② Redis Cache（雲端）
    data = get_redis(key)
    if data is not None:
        set_cache(key, data)
        return data

    # 🔥 ③ DB Cache
    df = load_from_db(symbol)
    if df is not None and len(df) > 50:
        set_cache(key, df)
        set_redis(key, df)
        return df

    # 🔥 ④ FinMind（retry + 限速）
    try:
        rate_limit("finmind", 1.2)
        df = fetch_with_retry(lambda: fetch_finmind(symbol))

        if df is not None and len(df) > 0:
            df = clean_df(df, symbol)
            save_to_db(symbol, df)
            set_cache(key, df)
            set_redis(key, df)
            return df
    except Exception as e:
        print(f"FinMind error: {e}")

    # 🔥 ⑤ Yahoo fallback
    try:
        rate_limit("yahoo", 1.0)
        df = fetch_with_retry(lambda: fetch_yahoo(symbol))

        if df is not None and len(df) > 0:
            df = clean_df(df, symbol)
            save_to_db(symbol, df)
            set_cache(key, df)
            set_redis(key, df)
            return df
    except Exception as e:
        print(f"Yahoo error: {e}")

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
