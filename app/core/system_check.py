import os

def check():

    status = {}

    status["model"] = os.path.exists("data/model_v3.pkl")
    status["portfolio"] = os.path.exists("portfolio.json")
    status["env"] = os.getenv("FINMIND_TOKEN") is not None

    return status
