from app.pipeline_v2 import run_pipeline
from app.core.selector import scan_market
from app.core.data_fetcher import get_stock_data
from app.core.portfolio import check_positions, summary
from app.core.performance_tracker import get_performance
from app.core.optimizer import suggest_params


def run_trade():

    trades = run_pipeline()

    prices = {}

    for t in trades:
        df = get_stock_data(t["symbol"])
        if df is not None:
            prices[t["symbol"]] = float(df["close"].iloc[-1])

    check_positions(prices)

    stats = summary(prices)

    result = "🚀 今日爆發股（已進場）\n\n"

    for t in trades:
        result += f"{t['symbol']} 勝率:{t['prob']}\n"

    result += f"\n💰 現金:{stats['cash']}\n總資產:{stats['equity']}\n持倉:{stats['positions']}\n"

    result += "\n" + get_performance()
    result += "\n" + suggest_params()

    return result


def run_observe():

    stocks = scan_market(mode="observe")

    result = "📊 今日推薦（觀察）\n\n"

    for s in stocks:
        result += f"{s['symbol']} 勝率:{s['score']}\n"

    return result


if __name__ == "__main__":
    print(run_trade())
