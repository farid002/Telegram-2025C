"""
Xərclər İzləyici Bot - Telegram bot əsas faylı

TODO:
1. Reply keyboard buttons
2. Handler-lər: start, add_expense, add_income, show_report
3. Inline keyboard ilə kateqoriya seçimi
4. user_states ilə vəziyyət idarəetməsi
"""

# TODO: Import-ları əlavə edin
# from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
# from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
# from database import Database
# from expense_manager import ExpenseManager
# from reports import Reports
# from config import BOT_TOKEN, EXPENSE_CATEGORIES

# TODO: Global obyektlər
# db = Database()
# expense_manager = ExpenseManager(db)
# reports = Reports(db)
# user_states = {}  # {user_id: {"action": "add_expense", "amount": 25.50}}


def get_main_keyboard():
    """
    Əsas klaviatura düymələri
    
    TODO: ReplyKeyboardMarkup yarat
    """
    # TODO: Keyboard
    return None


def get_category_keyboard():
    """Kateqoriya seçimi üçün düymələr"""
    # TODO: Kateqoriya keyboard
    return None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/start əmri - botu başladır"""
    # TODO: Start handler
    pass


async def add_expense(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Xərc əlavə etmə
    
    TODO:
    1. Məbləğ verilmişdirsə, kateqoriya seçimi göstər
    2. Yoxdursa, məbləğ yazılması tələb et
    3. user_states-də vəziyyəti saxla
    """
    # TODO: Xərc əlavə etmə handler
    pass


async def add_income(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gəlir əlavə etmə"""
    # TODO: Gəlir əlavə etmə handler
    pass


async def show_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Hesabat göstərir
    
    TODO:
    1. Hesabat növü seçimi düymələri (Günlük/Aylıq/Büdcə)
    """
    # TODO: Hesabat handler
    pass


async def show_expenses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xərcləri göstərir"""
    # TODO: Xərclər göstərmə handler
    pass


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Düymə basılmalarını idarə edir
    
    TODO:
    1. "category_X" - kateqoriya seçildi, xərc əlavə et
    2. "report_daily" - günlük hesabat
    3. "report_monthly" - aylıq hesabat
    4. "report_budget" - büdcə vəziyyəti
    """
    # TODO: Callback handler
    pass


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Mesajları idarə edir
    
    TODO:
    1. user_states-də vəziyyəti yoxla
    2. "add_expense" vəziyyətində - məbləğ qəbul et
    3. "add_income" vəziyyətində - məbləğ qəbul et
    4. Digər mesajlar üçün uyğun handler çağır
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