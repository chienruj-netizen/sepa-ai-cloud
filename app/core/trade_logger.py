import csv
import os

FILE = "trades.csv"

def log_trade(symbol, entry, exit_price, pnl):

    exists = os.path.exists(FILE)

    with open(FILE, "a", newline="") as f:
        writer = csv.writer(f)

        if not exists:
            writer.writerow(["symbol","entry","exit","pnl","result"])

        result = 1 if pnl > 0 else 0

        writer.writerow([symbol, entry, exit_price, pnl, result])
