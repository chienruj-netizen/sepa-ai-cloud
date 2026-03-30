import json
import os

FILE = "best_config.json"


def save_best(params):
    with open(FILE, "w") as f:
        json.dump(params, f)


def load_best():

    if not os.path.exists(FILE):
        return {
            "threshold": 0.6,
            "vol_ratio": 1.2
        }

    with open(FILE, "r") as f:
        return json.load(f)
