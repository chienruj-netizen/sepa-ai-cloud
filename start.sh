#!/bin/bash

echo "🚀 Starting Telegram Bot..."

# 🔥 防止重複啟動
if pgrep -f "app.interface.bot" > /dev/null
then
    echo "⚠️ Bot already running, exit"
    exit 1
fi

# 🔥 只允許這一個入口
python -m app.interface.bot

