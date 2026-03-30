import time
import yfinance as yf

from app.core.data_fetcher_raw import fetch_finmind
from app.core.ai_optimizer import CONFIG   # 🔥 動態參數


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


def simulate_trade(df):

    close = df["close"] if "close" in df.columns else df["Close"]
    high = df["high"] if "high" in df.columns else df["High"]
    low = df["low"] if "low" in df.columns else df["Low"]

    entry = float(close.iloc[-6])

    TP = CONFIG["tp"]   # 🔥 動態 TP
    SL = CONFIG["sl"]   # 🔥 動態 SL

    for i in range(-5, 0):

        h = float(high.iloc[i])
        l = float(low.iloc[i])

        # 🔥 停利
        if (h - entry) / entry >= TP:
            return TP, "TP"

        # 🔥 停損
        if (l - entry) / entry <= SL:
            return SL, "SL"

    final = float(close.iloc[-1])
    ret = (final - entry) / entry

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

            ret, reason = simulate_trade(df)

            # 🔥 做空處理
            if d.get("action") == "SELL":
                ret = -ret

            results.append({
                "symbol": symbol,
                "ret": float(ret),
                "reason": reason
            })

            print(f"📈 {symbol}: {round(ret,4)} ({reason})")

        except Exception as e:
            print(f"⚠️ 回測錯誤 {symbol}: {e}")

    return results
