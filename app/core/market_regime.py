from app.core.data_fetcher import fetch_stock_data

# 🔥 快取
_cache = {"data": None}

def get_market_regime():

    global _cache

    if _cache["data"] is not None:
        return _cache["data"]

    try:
        df = fetch_stock_data("^TWII")

        if df is None or len(df) < 50:
            return "sideways"

        close = df["close"].iloc[-1]
        ma20 = df["close"].rolling(20).mean().iloc[-1]

        if close > ma20 * 1.01:
            regime = "bull"
        elif close < ma20 * 0.99:
            regime = "bear"
        else:
            regime = "sideways"

        _cache["data"] = regime
        return regime

    except:
        return "sideways"
