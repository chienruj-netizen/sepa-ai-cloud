import requests
import os

FINMIND_TOKEN = os.getenv("FINMIND_API")


def get_institutional_flow(stock_id):

    try:
        url = "https://api.finmindtrade.com/api/v4/data"

        params = {
            "dataset": "TaiwanStockInstitutionalInvestorsBuySell",
            "data_id": stock_id,
            "start_date": "2024-01-01",
            "token": FINMIND_TOKEN
        }

        res = requests.get(url, params=params, timeout=10).json()

        data = res.get("data", [])

        if not data:
            return 0.0

        recent = data[-3:]

        total = 0.0

        for d in recent:
            buy = float(d.get("buy", 0))
            sell = float(d.get("sell", 0))

            total += (buy - sell)

        return total

    except Exception as e:
        print("❌ institution error:", e)
        return 0.0
