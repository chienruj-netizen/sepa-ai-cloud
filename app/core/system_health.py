import time
import requests

def check_api():
    try:
        requests.get("https://query1.finance.yahoo.com", timeout=3)
        return "OK"
    except:
        return "FAIL"

def system_status():
    return {
        "time": time.strftime("%H:%M:%S"),
        "api": check_api()
    }
