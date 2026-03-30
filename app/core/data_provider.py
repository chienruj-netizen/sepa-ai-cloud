from app.core.data_fetcher import get_stock_data

cache = {}

def get_data(code):
    if code not in cache:
        cache[code] = get_stock_data(code)
    return cache[code]
