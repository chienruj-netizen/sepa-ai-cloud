import requests

def get_tw_stocks():
    url = "https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL"

    try:
        data = requests.get(url, timeout=10).json()
        symbols = [d["Code"] + ".TW" for d in data if len(d["Code"]) == 4]
        return symbols
    except:
        return []
