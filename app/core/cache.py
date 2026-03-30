import time

CACHE = {}
TTL = {
    "1m": 60,
    "5m": 300,
    "1d": 600
}

def get_cache(key, tf="1d"):
    if key in CACHE:
        data, ts = CACHE[key]
        if time.time() - ts < TTL.get(tf, 600):
            return data
    return None

def set_cache(key, value):
    CACHE[key] = (value, time.time())
