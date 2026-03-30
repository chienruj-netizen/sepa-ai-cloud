import yfinance as yf

def get_market_regime():

    try:
        df = yf.download("^TWII", period="1mo")

        if df is None or len(df) < 20:
            return "sideways"

        close = df["Close"]

        if close.iloc[-1] > close.mean():
            return "bull"
        else:
            return "bear"

    except:
        return "sideways"
