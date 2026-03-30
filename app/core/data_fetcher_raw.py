import yfinance as yf
import requests
import pandas as pd
import os

FINMIND_TOKEN = os.getenv("FINMIND_TOKEN")

def fetch_yahoo(symbol):
    try:
        df = yf.download(symbol, period="6mo", progress=False, timeout=5)
        return df
    except Exception as e:
        print(f"❌ Yahoo error: {e}")
        return None


def fetch_finmind(symbol):
    try:
        url = "https://api.finmindtrade.com/api/v4/data"
        params = {
            "dataset": "TaiwanStockPrice",
            "data_id": symbol.replace(".TW", ""),
            "start_date": "2023-01-01",
            "token": FINMIND_TOKEN
        }

        resp = requests.get(url, params=params, timeout=5)

        if resp.status_code != 200:
            return None

        data = resp.json().get("data", [])
        if not data:
            return None

        df = pd.DataFrame(data)
        df = df.rename(columns={
            "open": "Open",
            "max": "High",
            "min": "Low",
            "close": "Close",
            "Trading_Volume": "Volume"
        })

        return df

    except Exception as e:
        print(f"❌ FinMind error: {e}")
        return None
