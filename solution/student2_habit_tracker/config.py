"""
Konfiqurasiya faylı - Bot token və digər parametrlər
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Token (BotFather-dən alınır)
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# Verilənlər bazası faylı
DATABASE_FILE = "habit_tracker.db"

# Xatırlatma vaxtı (saat)
REMINDER_HOUR = 20  # Gecə 20:00