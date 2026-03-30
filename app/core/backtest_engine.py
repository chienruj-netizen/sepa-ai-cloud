import time
import yfinance as yf
from app.core.data_fetcher_raw import fetch_finmind


TP = 0.05   # +5%
SL = -0.03  # -3%
MAX_HOLD_DAYS = 5


def safe_fetch(symbol):

    try:
        df = yf.download(symbol, period="6mo", interval="1d")

        if df is not None and len(df) > 30:
            if hasattr(df.columns, "levels"):
                df.columns = df.columns.get_level_values(0)

            df = df.rename(columns={
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Volume": "volume"
            })

            return df

    except Exception as e:
        print(f"⚠️ Yahoo失敗 {symbol}: {e}")

    print(f"🔁 使用 FinMind: {symbol}")
    return fetch_finmind(symbol)


def simulate_trade(close_prices):

    entry_price = float(close_prices.iloc[-6])

    for i in range(-5, 0):

        price = float(close_prices.iloc[i])
        ret = (price - entry_price) / entry_price

        # 🔥 TP
        if ret >= TP:
            return ret, "TP"

        # 🔥 SL
        if ret <= SL:
            return ret, "SL"

    # 🔥 到期出場
    final_price = float(close_prices.iloc[-1])
    ret = (final_price - entry_price) / entry_price

    return ret, "TIME"


def run_backtest(decisions):

    results = []

    for d in decisions:

        if d.get("position", 0) == 0:
            continue

        symbol = d.get("symbol")

        time.sleep(1)

        try:
            df = safe_fetch(symbol)

            if df is None or len(df) < 30:
                continue

            close = df["close"] if "close" in df.columns else df["Close"]

            ret, reason = simulate_trade(close)

            results.append({
                "symbol": symbol,
                "ret": float(ret),
                "reason": reason
            })

            print(f"📈 {symbol}: {round(ret,4)} ({reason})")

        except Exception as e:
            print(f"⚠️ 回測錯誤 {symbol}: {e}")

    return results
