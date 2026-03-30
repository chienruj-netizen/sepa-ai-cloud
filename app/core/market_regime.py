import yfinance as yf

def get_market_regime():

    try:
        df = yf.download("^TWII", period="6mo")

        close = df["Close"]

        ma20 = close.rolling(20).mean()
        ma60 = close.rolling(60).mean()

        # 🔥 牛市
        if ma20.iloc[-1] > ma60.iloc[-1] and close.iloc[-1] > ma20.iloc[-1]:
            return "bull"

        # 🔥 熊市
        elif ma20.iloc[-1] < ma60.iloc[-1] and close.iloc[-1] < ma20.iloc[-1]:
            return "bear"

        # 🔥 震盪
        else:
            return "sideways"

    except:
        return "unknown"
