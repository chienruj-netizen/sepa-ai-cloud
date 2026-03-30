from app.core.ml_predictor import predict
from app.core.data_fetcher import fetch_stock_data

SYMBOLS = ["2330.TW","2317.TW","1308.TW","2603.TW","2409.TW"]

def select_stocks():

    long_list = []
    short_list = []

    for symbol in SYMBOLS:

        df = fetch_stock_data(symbol)
        if df is None or len(df) < 50:
            continue

        close = df["close"].iloc[-1]
        ma20 = df["close"].rolling(20).mean().iloc[-1]

        features = [
            close / ma20
        ]

        long_score, short_score = predict(features)

        data = {
            "symbol": symbol,
            "price": close,
            "long": long_score,
            "short": short_score
        }

        if long_score > 0.7:
            long_list.append(data)

        if short_score > 0.7:
            short_list.append(data)

    long_list = sorted(long_list, key=lambda x: x["long"], reverse=True)
    short_list = sorted(short_list, key=lambda x: x["short"], reverse=True)

    return long_list[:3], short_list[:3]
