import numpy as np
import joblib

model = joblib.load("data/model_v3.pkl")

def predict(features):

    try:
        X = np.array(features).reshape(1, -1)
        prob = model.predict_proba(X)[0][1]
        return float(prob)

    except Exception as e:
        print("⚠️ predict error:", e)
        return 0.5
