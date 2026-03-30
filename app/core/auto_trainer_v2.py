import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
import joblib

MODEL_FILE = "model.pkl"
DATA_FILE = "trades.csv"

def retrain():
    if not os.path.exists(DATA_FILE):
        return

    df = pd.read_csv(DATA_FILE)
    df = df.dropna()

    if len(df) < 20:
        return

    X = df[["prob"]]
    y = df["result"] > 0

    model = RandomForestClassifier()
    model.fit(X, y)

    joblib.dump(model, MODEL_FILE)
