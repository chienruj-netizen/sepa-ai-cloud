import pandas as pd
from app.core.data_cache import load_from_db, save_to_db, init_db
from app.core.data_fetcher_raw import fetch_finmind, fetch_yahoo

init_db()


def clean_df(df, symbol):
    # 🔥 MultiIndex 修正
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df.columns.name = None

    # 🔥 欄位統一（全部小寫）
    df = df.rename(columns={
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "volume"
    })

    # 🔥 強制轉數字
    for col in ["open", "high", "low", "close", "volume"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # 🔥 加 symbol（如果需要）
    df["symbol"] = symbol

    df = df.dropna()

    return df


def get_stock_data(symbol):

    # cache
    df = load_from_db(symbol)
    if df is not None and len(df) > 50:
        return df

    # FinMind（忽略錯誤）
    try:
        df = fetch_finmind(symbol)
        if df is not None and len(df) > 0:
            df = clean_df(df, symbol)
            save_to_db(symbol, df)
            return df
    except:
        pass

    # Yahoo 主力
    df = fetch_yahoo(symbol)

    if df is not None and len(df) > 0:
        df = clean_df(df, symbol)
        save_to_db(symbol, df)
        return df

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
