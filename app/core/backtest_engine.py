import time
import yfinance as yf

from app.core.data_fetcher_raw import fetch_finmind


def safe_fetch(symbol):
    """
    🔥 Yahoo → FinMind fallback
    """

    try:
        df = yf.download(symbol, period="6mo", interval="1d")

        if df is not None and len(df) > 30:
            # flatten MultiIndex
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

    # 🔥 fallback FinMind
    print(f"🔁 使用 FinMind: {symbol}")
    df = fetch_finmind(symbol)

    return df


def run_backtest(decisions):

    results = []

    for d in decisions:

        # 🔥 只回測有進場
        if d.get("position", 0) == 0:
            continue

        symbol = d.get("symbol")

        if not symbol:
            continue

        # 🔥 防 Rate Limit
        time.sleep(1)

        try:
            df = safe_fetch(symbol)

            if df is None or len(df) < 30:
                print(f"⚠️ 無資料 {symbol}")
                continue

            close = df["close"] if "close" in df.columns else df["Close"]

            entry = close.iloc[-5]
            exit_price = close.iloc[-1]

            # 🔥 強制轉 float
            entry = float(entry.values[0]) if hasattr(entry, "values") else float(entry)
            exit_price = float(exit_price.values[0]) if hasattr(exit_price, "values") else float(exit_price)

            ret = (exit_price - entry) / entry

            results.append({
                "symbol": symbol,
                "ret": float(ret)
            })

            print(f"📈 回測 {symbol}: {round(ret,4)}")

        except Exception as e:
            print(f"⚠️ 回測錯誤 {symbol}: {e}")

    return results
