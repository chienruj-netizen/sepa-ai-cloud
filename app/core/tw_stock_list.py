import requests

def get_all_stocks():

    url = "https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL"

    try:
        data = requests.get(url).json()

        symbols = []

        for d in data:
            code = d.get("Code")
            if code and len(code) == 4:
                symbols.append(f"{code}.TW")

        return symbols

    except:
        return []
