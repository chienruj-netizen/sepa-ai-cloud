import requests
import os

FINMIND_TOKEN = os.getenv("FINMIND_API")


def get_institutional_flow(stock_id):

    url = "https://api.finmindtrade.com/api/v4/data"

    params = {
        "dataset": "TaiwanStockInstitutionalInvestorsBuySell",
        "data_id": stock_id,
        "start_date": "2024-01-01",
        "token": FINMIND_TOKEN
    }

    res = requests.get(url, params=params).json()

    data = res.get("data", [])

    if not data:
        return 0

    recent = data[-3:]

    total = sum([d["buy_sell"] for d in recent])

    return total
