#!/bin/bash

echo "🚀 Starting Telegram Bot..."

# 🔥 防止重複啟動（關鍵）
if pgrep -f "app.interface.bot" > /dev/null
then
    echo "⚠️ Bot already running, exit"
    exit 1
fi

exec python -m app.interface.bot
