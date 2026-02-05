"""
Xərclər İzləyici Bot - Telegram bot əsas faylı
"""
import logging
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from database import Database
from expense_manager import ExpenseManager
from reports import Reports
from config import BOT_TOKEN, EXPENSE_CATEGORIES

# Logging konfiqurasiyası
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Global obyektlər
db = Database()
expense_manager = ExpenseManager(db)
reports = Reports(db)

# İstifadəçi vəziyyəti
user_states = {}  # {user_id: "waiting_for_amount", "waiting_for_category", etc.}


def get_main_keyboard():
    """Əsas klaviatura düymələri"""
    keyboard = [
        [KeyboardButton("➕ Xərc Əlavə Et"), KeyboardButton("💰 Gəlir Əlavə Et")],
        [KeyboardButton("📊 Hesabatlar"), KeyboardButton("📋 Xərclərim")],
        [KeyboardButton("💵 Büdcə"), KeyboardButton("❓ Kömək")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_category_keyboard():
    """Kateqoriya seçimi üçün düymələr"""
    keyboard = []
    categories = list(EXPENSE_CATEGORIES.items())
    
    for i in range(0, len(categories), 2):
        row = []
        cat1, emoji1 = categories[i]
        row.append(InlineKeyboardButton(f"{emoji1} {cat1.capitalize()}", callback_data=f"category_{cat1}"))
        
        if i + 1 < len(categories):
            cat2, emoji2 = categories[i + 1]
            row.append(InlineKeyboardButton(f"{emoji2} {cat2.capitalize()}", callback_data=f"category_{cat2}"))
        keyboard.append(row)
    
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/start əmri - botu başladır"""
    user = update.effective_user
    user_id = user.id
    
    # İstifadəçini verilənlər bazasına əlavə et
    db.add_user(user_id, user.username, user.first_name)
    
    welcome_message = f"""
💰 Xərclər İzləyici Botuna Xoş Gəlmisiniz, {user.first_name}!

Bu bot ilə şəxsi maliyyənizi idarə edə bilərsiniz.

✨ Xüsusiyyətlər:
• Xərc və gəlir qeydiyyatı
• Kateqoriyalar üzrə izləmə
• Günlük və aylıq hesabatlar
• Büdcə təyin etmə və izləmə
• Balans hesablaması

📋 Əmrlər:
/start - Botu başlat
/addexpense - Xərc əlavə et
/addincome - Gəlir əlavə et
/report - Hesabat görün
/help - Kömək

Başlamaq üçün aşağıdakı düymələrdən istifadə edin!
    """
    
    await update.message.reply_text(welcome_message, reply_markup=get_main_keyboard())


async def add_expense(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xərc əlavə etmə"""
    user_id = update.effective_user.id
    
    if context.args:
        # Məbləğ verilmişdirsə
        try:
            amount = float(context.args[0])
            user_states[user_id] = {"action": "add_expense", "amount": amount}
            await update.message.reply_text(
                f"💰 Məbləğ: {amount:.2f} AZN\n\n"
                "İndi kateqoriya seçin:",
                reply_markup=get_category_keyboard()
            )
        except ValueError:
            await update.message.reply_text("❌ Düzgün məbləğ daxil edin! Məsələn: /addexpense 25.50")
    else:
        user_states[user_id] = {"action": "add_expense"}
        await update.message.reply_text(
            "💰 Xərc Əlavə Etmək\n\n"
            "Məbləği yazın (məsələn: 25.50) və ya /addexpense <məbləğ> formatında:"
        )


async def add_income(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gəlir əlavə etmə"""
    user_id = update.effective_user.id
    
    if context.args:
        try:
            amount = float(context.args[0])
            description = " ".join(context.args[1:]) if len(context.args) > 1 else "Gəlir"
            
            income_id = expense_manager.add_income(user_id, amount, description)
            if income_id:
                await update.message.reply_text(
                    f"✅ Gəlir uğurla əlavə edildi!\n\n"
                    f"💰 Məbləğ: {amount:.2f} AZN\n"
                    f"📝 Təsvir: {description}",
                    reply_markup=get_main_keyboard()
                )
                if user_id in user_states:
                    del user_states[user_id]
            else:
                await update.message.reply_text("❌ Xəta baş verdi.")
        except ValueError:
            await update.message.reply_text("❌ Düzgün məbləğ daxil edin!")
    else:
        user_states[user_id] = {"action": "add_income"}
        await update.message.reply_text(
            "💰 Gəlir Əlavə Etmək\n\n"
            "Məbləği yazın (məsələn: 1000) və ya /addincome <məbləğ> [təsvir] formatında:"
        )


async def show_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Hesabat göstərir"""
    user_id = update.effective_user.id
    
    keyboard = [
        [InlineKeyboardButton("📅 Günlük", callback_data="report_daily")],
        [InlineKeyboardButton("📆 Aylıq", callback_data="report_monthly")],
        [InlineKeyboardButton("💵 Büdcə Vəziyyəti", callback_data="report_budget")]
    ]
    
    await update.message.reply_text(
        "📊 Hesabat Növü Seçin:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def show_expenses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xərcləri göstərir"""
    user_id = update.effective_user.id
    
    # Son 10 xərc
    expenses = db.get_expenses(user_id)
    recent_expenses = expenses[:10]
    
    text = expense_manager.format_expense_list(recent_expenses)
    
    keyboard = [
        [InlineKeyboardButton("📊 Hesabatlar", callback_data="report_daily")],
        [InlineKeyboardButton("🔙 Geri", callback_data="back_to_menu")]
    ]
    
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Düymə basılmalarını idarə edir"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    data = query.data
    
    if data.startswith("category_"):
        # Kateqoriya seçildi
        category = data.replace("category_", "")
        
        if user_id in user_states and user_states[user_id].get("action") == "add_expense":
            amount = user_states[user_id].get("amount")
            if amount:
                expense_id = expense_manager.add_expense(user_id, amount, category, "")
                if expense_id:
                    emoji = EXPENSE_CATEGORIES.get(category, "📝")
                    await query.edit_message_text(
                        f"✅ Xərc uğurla əlavə edildi!\n\n"
                        f"{emoji} Kateqoriya: {category.capitalize()}\n"
                        f"💰 Məbləğ: {amount:.2f} AZN",
                        reply_markup=None
                    )
                    if user_id in user_states:
                        del user_states[user_id]
                else:
                    await query.answer("❌ Xəta baş verdi!", show_alert=True)
        return
    
    if data == "report_daily":
        report_text = reports.get_daily_report(user_id)
        keyboard = [[InlineKeyboardButton("🔙 Geri", callback_data="back_to_menu")]]
        await query.edit_message_text(report_text, reply_markup=InlineKeyboardMarkup(keyboard))
        return
    
    if data == "report_monthly":
        report_text = reports.get_monthly_report(user_id)
        keyboard = [[InlineKeyboardButton("🔙 Geri", callback_data="back_to_menu")]]
        await query.edit_message_text(report_text, reply_markup=InlineKeyboardMarkup(keyboard))
        return
    
    if data == "report_budget":
        report_text = reports.get_budget_status(user_id)
        keyboard = [[InlineKeyboardButton("🔙 Geri", callback_data="back_to_menu")]]
        await query.edit_message_text(report_text, reply_markup=InlineKeyboardMarkup(keyboard))
        return
    
    if data == "back_to_menu":
        await query.edit_message_text("Ana menyuya qayıtdınız.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mesajları idarə edir"""
    text = update.message.text
    user_id = update.effective_user.id
    
    if text == "➕ Xərc Əlavə Et":
        await add_expense(update, context)
    elif text == "💰 Gəlir Əlavə Et":
        await add_income(update, context)
    elif text == "📊 Hesabatlar":
        await show_report(update, context)
    elif text == "📋 Xərclərim":
        await show_expenses(update, context)
    elif text == "💵 Büdcə":
        await update.message.reply_text(
            "💵 Büdcə funksiyası tezliklə əlavə ediləcək.\n"
            "Hazırda hesabatlar bölməsindən büdcə vəziyyətini görə bilərsiniz.",
            reply_markup=get_main_keyboard()
        )
    elif text == "❓ Kömək":
        await help_command(update, context)
    else:
        # Vəziyyətə görə işlə
        if user_id in user_states:
            state = user_states[user_id]
            action = state.get("action")
            
            if action == "add_expense":
                try:
                    amount = float(text)
                    state["amount"] = amount
                    await update.message.reply_text(
                        f"💰 Məbləğ: {amount:.2f} AZN\n\n"
                        "İndi kateqoriya seçin:",
                        reply_markup=get_category_keyboard()
                    )
                except ValueError:
                    await update.message.reply_text("❌ Düzgün məbləğ daxil edin! (məsələn: 25.50)")
            
            elif action == "add_income":
                try:
                    amount = float(text)
                    income_id = expense_manager.add_income(user_id, amount, "Gəlir")
                    if income_id:
                        await update.message.reply_text(
                            f"✅ Gəlir uğurla əlavə edildi!\n\n"
                            f"💰 Məbləğ: {amount:.2f} AZN",
                            reply_markup=get_main_keyboard()
                        )
                        del user_states[user_id]
                except ValueError:
                    await update.message.reply_text("❌ Düzgün məbləğ daxil edin!")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kömək məlumatı"""
    message = """
📖 Kömək Məlumatı

💰 Bot Nədir?
Bu bot şəxsi maliyyənizi idarə etməyə kömək edir. Xərclərinizi və gəlirlərinizi qeyd edin, hesabatlar görün.

📋 Əsas Əmrlər:
/start - Botu başlat
/addexpense <məbləğ> - Xərc əlavə et
/addincome <məbləğ> - Gəlir əlavə et
/report - Hesabat görün
/help - Bu kömək mesajı

💡 Məsləhət: Hər gün xərclərinizi qeyd edin ki, daha dəqiq hesabatlar ala biləsiniz!
    """
    await update.message.reply_text(message, reply_markup=get_main_keyboard())


def main():
    """Botu işə salır"""
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN tapılmadı! .env faylında təyin edin.")
        return
    
    # Bot aplikasiyasını yaradır
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Əmrləri əlavə et
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("addexpense", add_expense))
    application.add_handler(CommandHandler("addincome", add_income))
    application.add_handler(CommandHandler("report", show_report))
    application.add_handler(CommandHandler("help", help_command))
    
    # Callback query handler
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Mesaj handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Botu işə sal
    logger.info("Bot işə salınır...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()