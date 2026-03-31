import pandas as pd
import os

FILE = "trades.csv"

def get_performance():

    if not os.path.exists(FILE):
        return "尚無交易紀錄"

    df = pd.read_csv(FILE)

    if len(df) == 0:
        return "尚無交易"

    win_rate = (df["result"] == 1).mean()
    avg_return = df["pnl"].mean()

    return f"""
📊 交易統計
總筆數：{len(df)}
勝率：{round(win_rate,2)}
平均報酬：{round(avg_return,3)}
"""
