import os
import pickle
import redis

REDIS_URL = os.getenv("REDIS_URL")

if REDIS_URL:
    r = redis.from_url(REDIS_URL)
else:
    r = None

TTL = 600  # 10分鐘

def get_redis(key):
    if not r:
        return None
    try:
        data = r.get(key)
        if data:
            return pickle.loads(data)
    except:
        return None
    return None

def set_redis(key, value):
    if not r:
        return
    try:
        r.setex(key, TTL, pickle.dumps(value))
    except:
        pass
