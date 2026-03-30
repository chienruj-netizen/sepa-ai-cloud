import pandas as pd
import os

FILE = "trades.csv"

def log_trade(symbol, entry, tp, sl, prob):
    row = {
        "symbol": symbol,
        "entry": entry,
        "tp": tp,
        "sl": sl,
        "prob": prob,
        "result": None
    }

    if not os.path.exists(FILE):
        df = pd.DataFrame([row])
    else:
        df = pd.read_csv(FILE)
        df = pd.concat([df, pd.DataFrame([row])])

    df.to_csv(FILE, index=False)


def update_results(price_map):
    if not os.path.exists(FILE):
        return

    df = pd.read_csv(FILE)

    for i, row in df.iterrows():
        if pd.isna(row["result"]):
            symbol = row["symbol"]

            if symbol in price_map:
                current = price_map[symbol]

                if current >= row["tp"]:
                    df.loc[i, "result"] = 1
                elif current <= row["sl"]:
                    df.loc[i, "result"] = -1

    df.to_csv(FILE, index=False)
