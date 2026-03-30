from app.pipeline import run_pipeline, run_market_scan

def analyze_single(symbol):
    return run_pipeline(symbol, use_gpt=True)

def get_today_picks():
    return run_market_scan()
