import requests
import os

FINMIND_TOKEN = os.getenv("FINMIND_API")


def safe_float(x):
    try:
        return float(x)
    except:
        return 0.0


def get_institutional_flow(stock_id):

    try:
        url = "https://api.finmindtrade.com/api/v4/data"

        params = {
            "dataset": "TaiwanStockInstitutionalInvestorsBuySell",
            "data_id": stock_id,
            "start_date": "2024-01-01",
            "token": FINMIND_TOKEN
        }

        res = requests.get(url, params=params, timeout=10)

        if res.status_code != 200:
            print("❌ FinMind HTTP error:", res.status_code)
            return 0.0

        data_json = res.json()
        data = data_json.get("data", [])

        if not data:
            return 0.0

        recent = data[-3:]

        total = 0.0

        for d in recent:
            buy = safe_float(d.get("buy"))
            sell = safe_float(d.get("sell"))

            total += (buy - sell)

        return float(total)

    except Exception as e:
        print("❌ institution error:", e)
        return 0.0
