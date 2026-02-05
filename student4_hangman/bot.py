"""
Adam Asma Oyunu Bot - Telegram bot əsas faylı

TODO:
1. Çətinlik səviyyəsi seçimi
2. Kateqoriya seçimi
3. Azərbaycan əlifbası düymələri
4. Oyun axını idarəetməsi
"""

# TODO: Import-ları əlavə edin
# from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
# from database import Database
# from game_logic import HangmanGame
# from word_database import get_word, get_categories, get_difficulties
# from config import BOT_TOKEN

# Azərbaycan əlifbası
# AZERBAIJAN_ALPHABET = "ABCÇDEƏFGĞHXIİJKQLMNOÖPRSŞTUÜVYZ"

# TODO: Global obyektlər
# db = Database()
# user_games = {}  # {user_id: HangmanGame}
# user_game_info = {}  # {user_id: {"difficulty": ..., "category": ...}}


def get_difficulty_keyboard():
    """Çətinlik səviyyəsi seçimi üçün düymələr"""
    # TODO: Çətinlik keyboard
    return None


def get_category_keyboard(difficulty):
    """Kateqoriya seçimi üçün düymələr"""
    # TODO: Kateqoriya keyboard
    return None


def get_letter_keyboard(game):
    """
    Hərf seçimi üçün düymələr
    
    TODO:
    1. Azərbaycan əlifbasından hərflər
    2. Artıq təxmin edilmiş hərflər üçün ❌
    3. Təxmin edilə bilən hərflər üçün normal düymə
    """
    # TODO: Hərf keyboard
    return None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/start əmri - botu başladır"""
    # TODO: Start handler
    pass


async def new_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Yeni oyun başladır"""
    # TODO: Yeni oyun handler
    pass


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Statistikaları göstərir"""
    # TODO: Stats handler
    pass


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Düymə basılmalarını idarə edir
    
    TODO:
    1. "difficulty_X" - çətinlik seçildi, kateqoriya göstər
    2. "category_X_Y" - kateqoriya seçildi, oyun başlat
    3. "letter_X" - hərf seçildi, təxmin et, nəticə göstər
    4. Oyun bitibsə, statistika yenilə
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