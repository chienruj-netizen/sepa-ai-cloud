import csv
import os
from datetime import datetime

FILE = "trade_log.csv"


def log_trade(symbol, action, entry, tp, sl):

    file_exists = os.path.isfile(FILE)

    with open(FILE, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["time", "symbol", "action", "entry", "tp", "sl"])

        writer.writerow([
            datetime.now(),
            symbol,
            action,
            entry,
            tp,
            sl
        ])


def calculate_win_rate():

    if not os.path.exists(FILE):
        return 0.5

    wins = 0
    total = 0

    with open(FILE, "r") as f:
        reader = csv.DictReader(f)

        for row in reader:
            total += 1

            entry = float(row["entry"])
            tp = float(row["tp"])

            # 👉 簡化版（之後可升級真實回測）
            if tp > entry:
                wins += 1

    if total == 0:
        return 0.5

    return round(wins / total, 2)
