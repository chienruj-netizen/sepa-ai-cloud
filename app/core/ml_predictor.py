import joblib
import os

MODEL_RETURN_PATH = "data/model_return.pkl"
MODEL_VOL_PATH = "data/model_vol.pkl"

model_return = None
model_vol = None


# ========================
# 🔥 載入模型（雙模型）
# ========================
def load_models():
    global model_return, model_vol

    if model_return is None and os.path.exists(MODEL_RETURN_PATH):
        model_return = joblib.load(MODEL_RETURN_PATH)

    if model_vol is None and os.path.exists(MODEL_VOL_PATH):
        model_vol = joblib.load(MODEL_VOL_PATH)


# ========================
# 🔥 預測（V7核心）
# ========================
def predict_return(features):

    load_models()

    # ❗ fallback（避免全系統壞掉）
    if model_return is None:
        return 0.01

    try:
        # 🔥 特徵工程（補齊）
        rsi = features.get("rsi", 50)
        vol_ratio = features.get("volume_ratio", 1)
        ma20 = features.get("ma20", 0)
        volatility = features.get("volatility", abs(rsi - 50))
        institution = features.get("institution", 0)

        X = [[
            rsi,
            vol_ratio,
            ma20,
            volatility,
            institution
        ]]

        # 🔥 主模型（報酬）
        pred_return = model_return.predict(X)[0]

        # 🔥 波動模型（風險）
        if model_vol:
            pred_vol = model_vol.predict(X)[0]
        else:
            pred_vol = 0

        # ========================
        # 🔥 Ensemble（關鍵）
        # ========================
        score = (0.7 * pred_return) - (0.3 * pred_vol)

        return float(score)

    except Exception as e:
        print("ML ERROR:", e)
        return 0.01
