import asyncio
from app.core.ml_trainer import train_model

async def auto_train():

    while True:

        print("🧠 開始每日模型更新")

        try:
            train_model()
        except Exception as e:
            print("❌ 訓練失敗:", e)

        # 🔥 每24小時更新
        await asyncio.sleep(86400)
