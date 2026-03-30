from app.core.data_fetcher import get_stock_data, get_realtime_price

def pick_candidates():

    stocks = ["2330", "2317", "2454"]

    results = []

    for s in stocks:

        df = get_stock_data(s)
        price = get_realtime_price(s)

        results.append({
            "symbol": f"{s}.TW",
            "df": df,
            "price": price
        })

    return results
