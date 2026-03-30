from app.core.data_fetcher import get_stock_data


def detect_reversal(symbol):

    df = get_stock_data(symbol)

    if df is None or len(df) < 60:
        return False

    try:
        close = df["close"] if "close" in df.columns else df["Close"]

        ma5 = close.rolling(5).mean()
        ma20 = close.rolling(20).mean()

        # 🔥 跌破短均線 + 轉弱
        cond1 = close.iloc[-1] < ma5.iloc[-1]
        cond2 = ma5.iloc[-1] < ma20.iloc[-1]

        return cond1 and cond2

    except:
        return False
