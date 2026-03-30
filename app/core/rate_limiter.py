import time

LAST_CALL = {}

def rate_limit(key, delay=1.0):
    now = time.time()
    last = LAST_CALL.get(key, 0)

    if now - last < delay:
        time.sleep(delay - (now - last))

    LAST_CALL[key] = time.time()
