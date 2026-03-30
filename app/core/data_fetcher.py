import requests
import pandas as pd
import os

FINMIND_TOKEN = os.getenv("FINMIND_API")


def get_stock_data(symbol):
    stock_id = symbol.replace(".TW", "")

    url = "https://api.finmindtrade.com/api/v4/data"

    params = {
        "dataset": "TaiwanStockPrice",
        "data_id": stock_id,
        "start_date": "2024-01-01",
        "token": FINMIND_TOKEN
    }

    resp = requests.get(url, params=params)
    data = resp.json()["data"]

    if not data:
        return None

    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    return df
