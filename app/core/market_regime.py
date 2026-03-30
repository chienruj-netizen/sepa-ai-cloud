from app.core.data_fetcher import fetch_stock_data

def get_market_regime():

    df = fetch_stock_data("^TWII")

    if df is None or len(df) < 50:
        return "sideways"

    close = df["close"].iloc[-1]
    ma20 = df["close"].rolling(20).mean().iloc[-1]

    if close > ma20 * 1.01:
        return "bull"
    elif close < ma20 * 0.99:
        return "bear"
    else:
        return "sideways"
