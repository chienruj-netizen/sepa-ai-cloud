def analyze_performance(df):

    if df.empty:
        return {
            "win_rate": 0,
            "avg_return": 0,
            "total_return": 0,
            "trades": 0
        }

    wins = df[df["return"] > 0]
    losses = df[df["return"] <= 0]

    win_rate = len(wins) / len(df)
    avg_return = df["return"].mean()
    total_return = (1 + df["return"]).prod() - 1

    return {
        "win_rate": round(win_rate, 2),
        "avg_return": round(avg_return, 4),
        "total_return": round(total_return, 4),
        "trades": len(df)
    }
