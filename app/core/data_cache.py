import sqlite3
import pandas as pd

DB_PATH = "data/market_cache.db"


# ========================
# 初始化資料庫
# ========================
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS stock_data (
        symbol TEXT,
        date TEXT,
        open REAL,
        high REAL,
        low REAL,
        close REAL,
        volume REAL,
        PRIMARY KEY (symbol, date)
    )
    """)

    conn.commit()
    conn.close()


# ========================
# 🔥 存資料（已修正）
# ========================
def save_to_db(symbol, df):

    conn = sqlite3.connect(DB_PATH)

    df = df.copy()

    # 🔥 index → date
    df = df.reset_index()

    # 🔥 扁平化欄位名稱（防 MultiIndex）
    df.columns = [str(col) for col in df.columns]

    # 🔥 統一欄位名稱
    df.rename(columns={
        "Date": "date",
        "Datetime": "date",
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "volume"
    }, inplace=True)

    df["symbol"] = symbol

    # 🔥 只保留需要欄位（避免炸）
    keep_cols = ["symbol", "date", "open", "high", "low", "close", "volume"]
    df = df[[col for col in keep_cols if col in df.columns]]

    # 🔥 防止重複寫入
    try:
        df.to_sql("stock_data", conn, if_exists="append", index=False)
    except Exception as e:
        print("DB insert warning:", e)

    conn.close()


# ========================
# 🔥 讀資料
# ========================
def load_from_db(symbol):

    conn = sqlite3.connect(DB_PATH)

    query = f"""
    SELECT * FROM stock_data
    WHERE symbol = '{symbol}'
    ORDER BY date
    """

    df = pd.read_sql(query, conn)

    conn.close()

    if df.empty:
        return None

    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)

    # 🔥 還原成 yfinance 格式
    df.rename(columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume"
    }, inplace=True)

    return df
