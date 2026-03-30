import sqlite3
import pandas as pd

DB_PATH = "data/market_cache.db"


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


def save_to_db(symbol, df):

    conn = sqlite3.connect(DB_PATH)
    df = df.copy()
    df.reset_index(inplace=True)

    df["symbol"] = symbol

    df.to_sql("stock_data", conn, if_exists="append", index=False)

    conn.close()


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

    return df
