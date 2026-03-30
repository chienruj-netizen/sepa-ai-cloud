import time
from app.core.data_cache import load_from_db, save_to_db
from app.core.data_cache import init_db

from app.core.data_fetcher_raw import fetch_finmind, fetch_yahoo

init_db()


def get_stock_data(symbol):

    # 1️⃣ 先查 cache
    df = load_from_db(symbol)

    if df is not None and len(df) > 50:
        return df

    # 2️⃣ FinMind
    df = fetch_finmind(symbol)

    if df is not None:
        save_to_db(symbol, df)
        return df

    # 3️⃣ Yahoo fallback
    df = fetch_yahoo(symbol)

    if df is not None:
        save_to_db(symbol, df)
        return df

    return None
