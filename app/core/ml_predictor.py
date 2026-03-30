import joblib
import numpy as np
import os

MODEL_FILE = "model.pkl"

model = None
if os.path.exists(MODEL_FILE):
    model = joblib.load(MODEL_FILE)

def predict(features):
    if model is None:
        return 0.5, 0.5

    X = np.array([features])

    prob = model.predict_proba(X)[0][1]

    long_score = prob
    short_score = 1 - prob

    return long_score, short_score
