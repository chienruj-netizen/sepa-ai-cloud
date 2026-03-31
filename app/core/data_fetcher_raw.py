import yfinance as yf
import pandas as pd


# ===== Yahoo =====
def fetch_yahoo(symbol):

    try:
        df = yf.download(symbol, period="6mo", interval="1d")

        if df is None or len(df) == 0:
            return None

        df = df.reset_index()

        return df

    except Exception as e:
        print("yahoo error:", e)
        return None


# ===== FinMind（先保留空）=====
def fetch_finmind(symbol):
    return None
