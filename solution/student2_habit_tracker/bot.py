"""
Gündəlik Vərdiş İzləyici Bot - Telegram bot əsas faylı
"""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from database import Database
from habit_manager import HabitManager
from statistics import Statistics
from config import BOT_TOKEN
from datetime import date

# Logging konfiqurasiyası
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Global obyektlər
db = Database()
habit_manager = HabitManager(db)
stats = Statistics(db)

# Emoji seçimləri
EMOJI_OPTIONS = ["✅", "💪", "📚", "🏃", "💧", "🧘", "🎯", "🌟", "🔥", "⭐"]


def get_main_keyboard():
    """Əsas klaviatura düymələri"""
    keyboard = [
        [KeyboardButton("📋 Vərdişlərim"), KeyboardButton("➕ Yeni Vərdiş")],
        [KeyboardButton("📊 Statistika"), KeyboardButton("📅 Təqvim")],
        [KeyboardButton("❓ Kömək")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/start əmri - botu başladır"""
    user = update.effective_user
    user_id = user.id
    
    # İstifadəçini verilənlər bazasına əlavə et
    db.add_user(user_id, user.username, user.first_name)
    
    welcome_message = f"""
🎯 Gündəlik Vərdiş İzləyici Botuna Xoş Gəlmisiniz, {user.first_name}!

Bu bot ilə gündəlik vərdişlərinizi izləyə, streak-lərinizi artıra bilərsiniz.

✨ Xüsusiyyətlər:
• Vərdiş əlavə etmə və silmə
• Gündəlik qeydiyyat (check-in)
• Streak izləməsi
• Aylıq statistika və təqvim
• Həftəlik hesabatlar

📋 Əmrlər:
/start - Botu başlat
/addhabit - Yeni vərdiş əlavə et
/myhabits - Vərdişlərinizi görün
/stats - Statistikaları görün
/help - Kömək

Başlamaq üçün aşağıdakı düymələrdən istifadə edin!
    """
    
    await update.message.reply_text(welcome_message, reply_markup=get_main_keyboard())


async def add_habit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Yeni vərdiş əlavə etmə"""
    user_id = update.effective_user.id
    
    if context.args:
        # Vərdiş adı verilmişdirsə
        habit_name = " ".join(context.args)
        emoji = "✅"
        habit_id = habit_manager.add_habit(user_id, habit_name, emoji)
        
        if habit_id:
            await update.message.reply_text(
                f"✅ Vərdiş '{habit_name}' uğurla əlavə edildi!\n\n"
                f"İndi hər gün bu vərdişi tamamladığınızda qeydiyyat edin.",
                reply_markup=get_main_keyboard()
            )
        else:
            await update.message.reply_text("❌ Xəta baş verdi. Yenidən cəhd edin.")
    else:
        # Emoji seçimi üçün düymələr
        keyboard = []
        for i in range(0, len(EMOJI_OPTIONS), 2):
            row = []
            row.append(InlineKeyboardButton(EMOJI_OPTIONS[i], callback_data=f"emoji_{EMOJI_OPTIONS[i]}"))
            if i + 1 < len(EMOJI_OPTIONS):
                row.append(InlineKeyboardButton(EMOJI_OPTIONS[i+1], callback_data=f"emoji_{EMOJI_OPTIONS[i+1]}"))
            keyboard.append(row)
        
        await update.message.reply_text(
            "📝 Yeni vərdiş əlavə etmək üçün:\n\n"
            "1. Vərdiş adını yazın (məsələn: 'Gündəlik idman')\n"
            "2. Və ya /addhabit <vərdiş adı> formatında yazın\n\n"
            "Əvvəlcə emoji seçin:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


async def my_habits(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Vərdişləri göstərir"""
    user_id = update.effective_user.id
    habits = habit_manager.get_user_habits(user_id)
    
    if not habits:
        await update.message.reply_text(
            "📝 Hələ heç bir vərdiş əlavə etməmisiniz.\n\n"
            "Yeni vərdiş əlavə etmək üçün /addhabit əmrindən istifadə edin.",
            reply_markup=get_main_keyboard()
        )
        return
    
    # Vərdişlər üçün düymələr
    keyboard = []
    for habit_id, habit_name, emoji in habits:
        stats = habit_manager.get_habit_stats(habit_id)
        button_text = f"{emoji} {habit_name} (🔥{stats['streak']})"
        keyboard.append([InlineKeyboardButton(button_text, callback_data=f"habit_{habit_id}")])
    
    keyboard.append([InlineKeyboardButton("➕ Yeni Vərdiş", callback_data="add_new_habit")])
    
    text = habit_manager.format_habits_list(habits)
    text += "\nVərdiş seçmək üçün düyməni basın:"
    
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


async def show_statistics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Statistikaları göstərir"""
    user_id = update.effective_user.id
    habits = habit_manager.get_user_habits(user_id)
    
    if not habits:
        await update.message.reply_text("📊 Hələ heç bir vərdiş yoxdur.")
        return
    
    text = "📊 Ümumi Statistika\n\n"
    
    for habit_id, habit_name, emoji in habits:
        stats_data = habit_manager.get_habit_stats(habit_id)
        text += f"{emoji} {habit_name}\n"
        text += f"   🔥 Streak: {stats_data['streak']} gün\n"
        text += f"   📊 Cəmi qeydiyyat: {stats_data['total']}\n"
        text += f"   📅 Bu ay: {stats_data['this_month']}\n"
        text += f"   📈 Son 7 gün: {stats_data['week']}/7\n"
        text += f"   📈 Son 30 gün: {stats_data['month']}/30\n\n"
    
    await update.message.reply_text(text, reply_markup=get_main_keyboard())


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Düymə basılmalarını idarə edir"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    data = query.data
    
    if data.startswith("emoji_"):
        # Emoji seçildi
        emoji = data.replace("emoji_", "")
        context.user_data['selected_emoji'] = emoji
        await query.edit_message_text(
            f"✅ Emoji seçildi: {emoji}\n\n"
            "İndi vərdiş adını yazın və ya /addhabit <ad> formatında göndərin."
        )
        return
    
    if data.startswith("habit_"):
        # Vərdiş seçildi
        habit_id = int(data.replace("habit_", ""))
        habits = habit_manager.get_user_habits(user_id)
        habit_info = next((h for h in habits if h[0] == habit_id), None)
        
        if habit_info:
            habit_name = habit_info[1]
            emoji = habit_info[2]
            stats_data = habit_manager.get_habit_stats(habit_id)
            
            keyboard = [
                [InlineKeyboardButton("✅ Bu Gün Qeydiyyat Et", callback_data=f"checkin_{habit_id}")],
                [InlineKeyboardButton("📊 Statistika", callback_data=f"stats_{habit_id}")],
                [InlineKeyboardButton("📅 Təqvim", callback_data=f"calendar_{habit_id}")],
                [InlineKeyboardButton("🗑️ Sil", callback_data=f"delete_{habit_id}")],
                [InlineKeyboardButton("🔙 Geri", callback_data="back_to_habits")]
            ]
            
            text = f"{emoji} {habit_name}\n\n"
            text += f"🔥 Streak: {stats_data['streak']} gün\n"
            text += f"📊 Cəmi: {stats_data['total']} qeydiyyat\n"
            text += f"📅 Bu ay: {stats_data['this_month']} qeydiyyat\n"
            
            await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    
    if data.startswith("checkin_"):
        # Qeydiyyat et
        habit_id = int(data.replace("checkin_", ""))
        success = habit_manager.checkin_habit(habit_id)
        
        if success:
            stats_data = habit_manager.get_habit_stats(habit_id)
            await query.answer("✅ Bu gün üçün qeydiyyat edildi!", show_alert=True)
            
            habits = habit_manager.get_user_habits(user_id)
            habit_info = next((h for h in habits if h[0] == habit_id), None)
            if habit_info:
                emoji = habit_info[2]
                habit_name = habit_info[1]
                
                keyboard = [
                    [InlineKeyboardButton("✅ Bu Gün Qeydiyyat Et", callback_data=f"checkin_{habit_id}")],
                    [InlineKeyboardButton("📊 Statistika", callback_data=f"stats_{habit_id}")],
                    [InlineKeyboardButton("📅 Təqvim", callback_data=f"calendar_{habit_id}")],
                    [InlineKeyboardButton("🗑️ Sil", callback_data=f"delete_{habit_id}")],
                    [InlineKeyboardButton("🔙 Geri", callback_data="back_to_habits")]
                ]
                
                text = f"{emoji} {habit_name}\n\n"
                text += f"🔥 Streak: {stats_data['streak']} gün\n"
                text += f"📊 Cəmi: {stats_data['total']} qeydiyyat\n"
                text += f"📅 Bu ay: {stats_data['this_month']} qeydiyyat\n"
                
                await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            await query.answer("ℹ️ Bu gün üçün artıq qeydiyyat edilib!", show_alert=True)
    
    if data.startswith("delete_"):
        # Vərdişi sil
        habit_id = int(data.replace("delete_", ""))
        keyboard = [
            [InlineKeyboardButton("✅ Bəli, Sil", callback_data=f"confirm_delete_{habit_id}")],
            [InlineKeyboardButton("❌ Xeyr", callback_data=f"habit_{habit_id}")]
        ]
        await query.edit_message_text(
            "⚠️ Bu vərdişi silmək istədiyinizə əminsiniz?\n\n"
            "Bütün qeydiyyatlar silinəcək!",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    if data.startswith("confirm_delete_"):
        # Silməni təsdiqlə
        habit_id = int(data.replace("confirm_delete_", ""))
        success = habit_manager.delete_habit(habit_id, user_id)
        
        if success:
            await query.edit_message_text("✅ Vərdiş silindi!")
            await my_habits(update, context)
        else:
            await query.answer("❌ Xəta baş verdi!", show_alert=True)
    
    if data == "back_to_habits":
        # Vərdişlər siyahısına qayıt
        habits = habit_manager.get_user_habits(user_id)
        keyboard = []
        for habit_id, habit_name, emoji in habits:
            stats_data = habit_manager.get_habit_stats(habit_id)
            button_text = f"{emoji} {habit_name} (🔥{stats_data['streak']})"
            keyboard.append([InlineKeyboardButton(button_text, callback_data=f"habit_{habit_id}")])
        
        keyboard.append([InlineKeyboardButton("➕ Yeni Vərdiş", callback_data="add_new_habit")])
        
        text = habit_manager.format_habits_list(habits)
        text += "\nVərdiş seçmək üçün düyməni basın:"
        
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    
    if data == "add_new_habit":
        await query.edit_message_text(
            "📝 Yeni vərdiş əlavə etmək üçün /addhabit <vərdiş adı> yazın."
        )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mesajları idarə edir"""
    text = update.message.text
    
    if text == "📋 Vərdişlərim":
        await my_habits(update, context)
    elif text == "➕ Yeni Vərdiş":
        await add_habit(update, context)
    elif text == "📊 Statistika":
        await show_statistics(update, context)
    elif text == "📅 Təqvim":
        await update.message.reply_text(
            "📅 Təqvim görünüşü üçün vərdiş seçin: /myhabits",
            reply_markup=get_main_keyboard()
        )
    elif text == "❓ Kömək":
        await help_command(update, context)
    else:
        # Vərdiş adı ola bilər
        if 'selected_emoji' in context.user_data:
            emoji = context.user_data['selected_emoji']
            habit_id = habit_manager.add_habit(update.effective_user.id, text, emoji)
            if habit_id:
                del context.user_data['selected_emoji']
                await update.message.reply_text(
                    f"✅ Vərdiş '{text}' uğurla əlavə edildi!",
                    reply_markup=get_main_keyboard()
                )
            else:
                await update.message.reply_text("❌ Xəta baş verdi.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kömək məlumatı"""
    message = """
📖 Kömək Məlumatı

🎯 Bot Nədir?
Bu bot gündəlik vərdişlərinizi izləməyə kömək edir. Hər gün vərdişlərinizi tamamladıqda qeydiyyat edin və streak-lərinizi artırın!

📋 Əsas Əmrlər:
/start - Botu başlat
/addhabit <ad> - Yeni vərdiş əlavə et
/myhabits - Vərdişlərinizi görün
/stats - Statistikaları görün
/help - Bu kömək mesajı

✨ Xüsusiyyətlər:
• Vərdiş əlavə etmə və silmə
• Gündəlik qeydiyyat
• Streak izləməsi
• Aylıq statistika
• Təqvim görünüşü

💡 Məsləhət: Hər gün eyni vaxtda qeydiyyat edin ki, streak-ləriniz kəsilməsin!
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
    application.add_handler(CommandHandler("addhabit", add_habit))
    application.add_handler(CommandHandler("myhabits", my_habits))
    application.add_handler(CommandHandler("stats", show_statistics))
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