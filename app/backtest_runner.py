from app.core.backtest_engine import run_backtest
from app.core.performance import analyze_performance, long_short_split


def run():

    df = run_backtest("2330.TW")

    overall = analyze_performance(df)
    split = long_short_split(df)

    print("\n📊 總體績效")
    print(overall)

    print("\n🟢 做多")
    print(split["long"])

    print("\n🔴 做空")
    print(split["short"])
