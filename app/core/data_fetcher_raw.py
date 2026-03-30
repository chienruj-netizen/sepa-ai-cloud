import requests
import pandas as pd
import yfinance as yf
import os


def fetch_finmind(symbol):

    token = os.getenv("FINMIND_TOKEN")

    if not token:
        return None

    try:
        stock_id = symbol.replace(".TW", "")

        url = "https://api.finmindtrade.com/api/v4/data"
        params = {
            "dataset": "TaiwanStockPrice",
            "data_id": stock_id,
            "start_date": "2023-01-01",
            "token": token
        }

        res = requests.get(url, params=params)
        data = res.json()["data"]

        if not data:
            return None

        df = pd.DataFrame(data)
        df["date"] = pd.to_datetime(df["date"])
        df.set_index("date", inplace=True)

        df.rename(columns={
            "open": "Open",
            "high": "High",
            "low": "Low",
            "close": "Close",
            "volume": "Volume"
        }, inplace=True)

        return df[["Open", "High", "Low", "Close", "Volume"]]

    except:
        return None


def fetch_yahoo(symbol):

    try:
        df = yf.download(symbol, period="1y")

        if df.empty:
            return None

        return df

    except:
        return None
