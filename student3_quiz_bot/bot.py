"""
Viktorina Master Bot - Telegram bot əsas faylı

TODO:
1. Handler-ləri yazın: start, quiz, stats, leaderboard
2. Inline keyboard ilə kateqoriya seçimi
3. Cavab düymələri (A, B, C, D)
4. Callback query handler
"""

# TODO: Import-ları əlavə edin
# from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
# from database import Database
# from quiz_engine import QuizEngine
# from questions import get_categories
# from config import BOT_TOKEN

# TODO: Global obyektlər
# db = Database()
# quiz_engine = QuizEngine()


def get_category_keyboard():
    """
    Kateqoriya seçimi üçün düymələr
    
    TODO:
    1. Bütün kateqoriyaları al
    2. Hər kateqoriya üçün emoji və düymə yarat
    3. InlineKeyboardMarkup qaytar
    """
    # TODO: Kateqoriya keyboard
    return None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/start əmri - botu başladır"""
    # TODO: Start handler
    pass


async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Viktorina başladır
    
    TODO:
    1. Aktiv oyun varsa, bitir
    2. Kateqoriya seçimi düymələri göstər
    """
    # TODO: Quiz handler
    pass


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Statistikaları göstərir"""
    # TODO: Stats handler
    pass


async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Liderboard göstərir
    
    TODO:
    1. get_leaderboard() çağır
    2. Formatlaşdırılmış siyahı göstər
    """
    # TODO: Leaderboard handler
    pass


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Düymə basılmalarını idarə edir
    
    TODO:
    1. "category_X" - kateqoriya seçildi, viktorina başlat
    2. "answer_X" - cavab verildi, nəticə göstər, növbəti sual
    3. "statistics" - statistika göstər
    4. "leaderboard" - liderboard göstər
    5. Oyun bitibsə, nəticə göstər və statistika yenilə
    """
    # TODO: Callback handler
    pass


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kömək məlumatı"""
    # TODO: Kömək mesajı
    pass


def main():
    """Botu işə salır"""
    # TODO: Application yarat və handler-ləri əlavə et
    pass


if __name__ == "__main__":
    main()