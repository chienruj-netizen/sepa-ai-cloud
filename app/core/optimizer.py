import pandas as pd
import os

FILE = "trades.csv"

def suggest_params():

    if not os.path.exists(FILE):
        return "尚無數據"

    df = pd.read_csv(FILE)

    if len(df) == 0:
        return "尚無交易"

    win_rate = (df["result"] == 1).mean()

    if win_rate < 0.5:
        return "🔻 勝率低 → 提高條件：vol_ratio > 1.5"
    elif win_rate < 0.6:
        return "⚖️ 正常 → 微調 acceleration 條件"
    else:
        return "🚀 勝率佳 → 可增加倉位"
