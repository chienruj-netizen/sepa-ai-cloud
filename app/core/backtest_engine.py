import yfinance as yf


def run_backtest(decisions):

    results = []

    for d in decisions:

        # 🔥 只回測有進場的（關鍵升級）
        if d.get("position", 0) == 0:
            continue

        symbol = d.get("symbol")

        if not symbol:
            continue

        try:
            df = yf.download(symbol, period="6mo", interval="1d")

            if df is None or len(df) < 30:
                continue

            # 🔥 解 MultiIndex
            if hasattr(df.columns, "levels"):
                df.columns = df.columns.get_level_values(0)

            close = df["Close"]

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
