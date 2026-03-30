import pandas as pd
import os

FILE = "trades.csv"

def get_performance():
    if not os.path.exists(FILE):
        return {}

    df = pd.read_csv(FILE)

    df = df.dropna()

    if len(df) == 0:
        return {}

    win_rate = (df["result"] == 1).mean()
    avg_return = df["result"].mean()

    return {
        "trades": len(df),
        "win_rate": round(win_rate, 2),
        "avg_return": round(avg_return, 3)
    }
