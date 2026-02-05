"""
Gündəlik Vərdiş İzləyici Bot - Telegram bot əsas faylı

TODO:
1. Reply keyboard buttons yaradın
2. Handler-ləri yazın: start, add_habit, my_habits, show_statistics
3. Callback query handler - emoji seçimi, vərdiş seçimi, qeydiyyat
4. Message handler - vərdiş adı qəbulu
"""

# TODO: Import-ları əlavə edin
# from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
# from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
# from database import Database
# from habit_manager import HabitManager
# from statistics import Statistics
# from config import BOT_TOKEN

# TODO: Global obyektlər
# db = Database()
# habit_manager = HabitManager(db)
# stats = Statistics(db)
# user_states = {}  # İstifadəçi vəziyyəti


def get_main_keyboard():
    """
    Əsas klaviatura düymələri
    
    TODO: ReplyKeyboardMarkup yarat
    """
    # TODO: Keyboard yaratma
    return None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/start əmri - botu başladır"""
    # TODO: Start handler
    pass


async def add_habit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Yeni vərdiş əlavə etmə
    
    TODO:
    1. Emoji seçimi düymələri göstər
    2. user_states-də vəziyyəti saxla
    """
    # TODO: Vərdiş əlavə etmə handler
    pass


async def my_habits(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Vərdişləri göstərir
    
    TODO:
    1. İstifadəçinin vərdişlərini al
    2. Hər vərdiş üçün inline button yarat
    3. Siyahı göstər
    """
    # TODO: Vərdişlər göstərmə handler
    pass


async def show_statistics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Statistikaları göstərir"""
    # TODO: Statistika handler
    pass


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Düymə basılmalarını idarə edir
    
    TODO:
    1. Emoji seçimi
    2. Vərdiş seçimi
    3. Qeydiyyat etmə
    4. Statistika göstərmə
    5. Vərdiş silmə
    """
    # TODO: Callback handler
    pass


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Mesajları idarə edir
    
    TODO:
    1. user_states-də vəziyyəti yoxla
    2. "add_expense" vəziyyətində - vərdiş adı qəbul et
    3. Digər mesajlar üçün uyğun handler çağır
    """
    # TODO: Message handler
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