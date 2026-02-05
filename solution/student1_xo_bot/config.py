"""
Konfiqurasiya faylı - Bot token və digər parametrlər
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Token (BotFather-dən alınır)
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# Verilənlər bazası faylı
DATABASE_FILE = "xo_bot.db"

# Logging konfiqurasiyası
LOG_LEVEL = "INFO"