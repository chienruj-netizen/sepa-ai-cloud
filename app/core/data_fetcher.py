import requests
import os

FINMIND_TOKEN = os.getenv("FINMIND_API")


def get_price(symbol):

    url = "https://api.finmindtrade.com/api/v4/data"

    params = {
        "dataset": "TaiwanStockPrice",
        "data_id": symbol.replace(".TW", ""),
        "start_date": "2024-01-01",
        "token": FINMIND_TOKEN
    }

    res = requests.get(url, params=params)
    data = res.json()

    if "data" not in data or len(data["data"]) == 0:
        return None

    latest = data["data"][-1]

    return {
        "price": latest["close"],
        "volume": latest["Trading_Volume"]
    }
