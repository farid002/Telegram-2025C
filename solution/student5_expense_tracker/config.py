"""
Konfiqurasiya faylı - Bot token və digər parametrlər
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Token (BotFather-dən alınır)
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# Verilənlər bazası faylı
DATABASE_FILE = "expense_tracker.db"

# Xərc kateqoriyaları
EXPENSE_CATEGORIES = {
    "yemək": "🍔",
    "nəqliyyat": "🚗",
    "əyləncə": "🎬",
    "sağlamlıq": "💊",
    "alış-veriş": "🛒",
    "təhsil": "📚",
    "kommunal": "🏠",
    "digər": "📝"
}