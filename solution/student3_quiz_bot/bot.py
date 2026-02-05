"""
Viktorina Master Bot - Telegram bot əsas faylı
"""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from database import Database
from quiz_engine import QuizEngine
from questions import get_categories
from config import BOT_TOKEN

# Logging konfiqurasiyası
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Global obyektlər
db = Database()
quiz_engine = QuizEngine()

# Kateqoriya emojiləri
CATEGORY_EMOJIS = {
    "riyaziyyat": "🔢",
    "tarix": "📜",
    "elm": "🔬",
    "ədəbiyyat": "📚",
    "idman": "⚽",
    "coğrafiya": "🌍"
}


def get_category_keyboard():
    """Kateqoriya seçimi üçün düymələr"""
    categories = get_categories()
    keyboard = []
    
    for i in range(0, len(categories), 2):
        row = []
        cat1 = categories[i]
        emoji1 = CATEGORY_EMOJIS.get(cat1, "📝")
        row.append(InlineKeyboardButton(
            f"{emoji1} {cat1.capitalize()}",
            callback_data=f"category_{cat1}"
        ))
        
        if i + 1 < len(categories):
            cat2 = categories[i + 1]
            emoji2 = CATEGORY_EMOJIS.get(cat2, "📝")
            row.append(InlineKeyboardButton(
                f"{emoji2} {cat2.capitalize()}",
                callback_data=f"category_{cat2}"
            ))
        keyboard.append(row)
    
    keyboard.append([InlineKeyboardButton("📊 Statistika", callback_data="statistics")])
    keyboard.append([InlineKeyboardButton("🏆 Liderboard", callback_data="leaderboard")])
    
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/start əmri - botu başladır"""
    user = update.effective_user
    user_id = user.id
    
    # İstifadəçini verilənlər bazasına əlavə et
    db.add_user(user_id, user.username, user.first_name)
    
    welcome_message = f"""
🎯 Viktorina Master Botuna Xoş Gəlmisiniz, {user.first_name}!

Bu bot ilə müxtəlif mövzularda biliklərinizi yoxlaya bilərsiniz.

✨ Xüsusiyyətlər:
• Müxtəlif kateqoriyalar (riyaziyyat, tarix, elm, ədəbiyyat, idman, coğrafiya)
• 10 suallı viktorinalar
• Xal sistemi və statistika
• Liderboard

📋 Əmrlər:
/start - Botu başlat
/quiz - Viktorina başlat
/stats - Statistikaları görün
/leaderboard - Liderboard görün
/help - Kömək

Başlamaq üçün /quiz əmrindən istifadə edin!
    """
    
    await update.message.reply_text(welcome_message)


async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Viktorina başladır"""
    user_id = update.effective_user.id
    
    # Aktiv oyun varsa, onu bitir
    if user_id in quiz_engine.user_quizzes:
        quiz_engine.end_quiz(user_id)
    
    message = "📚 Viktorina Kateqoriyası Seçin:\n\nAşağıdakı kateqoriyalardan birini seçin:"
    await update.message.reply_text(message, reply_markup=get_category_keyboard())


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Statistikaları göstərir"""
    user_id = update.effective_user.id
    stats_data = db.get_statistics(user_id)
    
    if stats_data:
        total_games, total_score, total_questions, best_score = stats_data
        avg_score = (total_score / total_games * 10) if total_games > 0 else 0
        
        message = f"""
📊 Sizin Statistikalarınız:

🎮 Oynanılan oyunlar: {total_games}
✅ Cəmi xal: {total_score}
📝 Cəmi suallar: {total_questions}
🏆 Ən yaxşı nəticə: {best_score}/10
📈 Orta xal: {avg_score:.1f}/10
        """
    else:
        message = "📊 Hələ heç bir oyun oynamamısınız. /quiz ilə başlayın!"
    
    await update.message.reply_text(message)


async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Liderboard göstərir"""
    leaders = db.get_leaderboard(10)
    
    if not leaders:
        await update.message.reply_text("🏆 Hələ liderboard yoxdur. İlk olun!")
        return
    
    message = "🏆 Liderboard (Ən Yaxşı Nəticələr):\n\n"
    
    medals = ["🥇", "🥈", "🥉"]
    for i, (first_name, username, best_score, total_games) in enumerate(leaders, 1):
        medal = medals[i-1] if i <= 3 else f"{i}."
        name = first_name or username or "Anonim"
        message += f"{medal} {name}: {best_score}/10 ({total_games} oyun)\n"
    
    await update.message.reply_text(message)


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Düymə basılmalarını idarə edir"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    data = query.data
    
    if data == "statistics":
        stats_data = db.get_statistics(user_id)
        if stats_data:
            total_games, total_score, total_questions, best_score = stats_data
            avg_score = (total_score / total_games * 10) if total_games > 0 else 0
            
            message = f"""
📊 Sizin Statistikalarınız:

🎮 Oynanılan oyunlar: {total_games}
✅ Cəmi xal: {total_score}
📝 Cəmi suallar: {total_questions}
🏆 Ən yaxşı nəticə: {best_score}/10
📈 Orta xal: {avg_score:.1f}/10
            """
        else:
            message = "📊 Hələ heç bir oyun oynamamısınız."
        
        keyboard = [[InlineKeyboardButton("🔙 Geri", callback_data="back_to_menu")]]
        await query.edit_message_text(message, reply_markup=InlineKeyboardMarkup(keyboard))
        return
    
    if data == "leaderboard":
        leaders = db.get_leaderboard(10)
        if not leaders:
            message = "🏆 Hələ liderboard yoxdur."
        else:
            message = "🏆 Liderboard (Ən Yaxşı Nəticələr):\n\n"
            medals = ["🥇", "🥈", "🥉"]
            for i, (first_name, username, best_score, total_games) in enumerate(leaders, 1):
                medal = medals[i-1] if i <= 3 else f"{i}."
                name = first_name or username or "Anonim"
                message += f"{medal} {name}: {best_score}/10 ({total_games} oyun)\n"
        
        keyboard = [[InlineKeyboardButton("🔙 Geri", callback_data="back_to_menu")]]
        await query.edit_message_text(message, reply_markup=InlineKeyboardMarkup(keyboard))
        return
    
    if data == "back_to_menu":
        message = "📚 Viktorina Kateqoriyası Seçin:\n\nAşağıdakı kateqoriyalardan birini seçin:"
        await query.edit_message_text(message, reply_markup=get_category_keyboard())
        return
    
    if data.startswith("category_"):
        # Kateqoriya seçildi
        category = data.replace("category_", "")
        quiz_data = quiz_engine.start_quiz(user_id, category)
        
        if not quiz_data:
            await query.answer("❌ Xəta baş verdi!", show_alert=True)
            return
        
        question = quiz_engine.get_current_question(user_id)
        if question:
            question_text = quiz_engine.format_question(
                question,
                quiz_data["current_question"] + 1,
                len(quiz_data["questions"])
            )
            
            # Cavab düymələri
            keyboard = []
            options_emoji = ["A", "B", "C", "D"]
            for i, option in enumerate(question['options']):
                keyboard.append([InlineKeyboardButton(
                    f"{options_emoji[i]}) {option}",
                    callback_data=f"answer_{i}"
                )])
            
            await query.edit_message_text(question_text, reply_markup=InlineKeyboardMarkup(keyboard))
        return
    
    if data.startswith("answer_"):
        # Cavab verildi
        if user_id not in quiz_engine.user_quizzes:
            await query.answer("❌ Aktiv oyun yoxdur!", show_alert=True)
            return
        
        answer_index = int(data.replace("answer_", ""))
        result = quiz_engine.answer_question(user_id, answer_index)
        
        if result:
            # Cavab nəticəsi
            if result["is_correct"]:
                feedback = "✅ Düzgün cavab!"
            else:
                correct_option = ["A", "B", "C", "D"][result["correct_answer"]]
                feedback = f"❌ Səhv! Düzgün cavab: {correct_option}"
            
            feedback += f"\n\n📊 Xal: {result['score']}/{result['total']}"
            
            await query.answer(feedback, show_alert=True)
            
            # Növbəti sual
            if not quiz_engine.is_finished(user_id):
                question = quiz_engine.get_current_question(user_id)
                if question:
                    quiz_data = quiz_engine.user_quizzes[user_id]
                    question_text = quiz_engine.format_question(
                        question,
                        quiz_data["current_question"] + 1,
                        len(quiz_data["questions"])
                    )
                    
                    keyboard = []
                    options_emoji = ["A", "B", "C", "D"]
                    for i, option in enumerate(question['options']):
                        keyboard.append([InlineKeyboardButton(
                            f"{options_emoji[i]}) {option}",
                            callback_data=f"answer_{i}"
                        )])
                    
                    await query.edit_message_text(question_text, reply_markup=InlineKeyboardMarkup(keyboard))
            else:
                # Oyun bitdi
                results = quiz_engine.end_quiz(user_id)
                db.save_game(user_id, results["category"], results["score"], results["total"])
                db.update_statistics(user_id, results["score"], results["total"])
                
                percentage = results["percentage"]
                if percentage >= 90:
                    emoji = "🏆"
                    message = "Əla nəticə!"
                elif percentage >= 70:
                    emoji = "🎉"
                    message = "Yaxşı nəticə!"
                elif percentage >= 50:
                    emoji = "👍"
                    message = "Orta nəticə!"
                else:
                    emoji = "💪"
                    message = "Davam edin!"
                
                result_text = f"""
{emoji} {message}

📊 Viktorina Nəticəsi:
✅ Düzgün cavablar: {results['score']}/{results['total']}
📈 Faiz: {percentage:.1f}%

Yeni viktorina başlatmaq istəyirsiniz?
                """
                
                keyboard = [
                    [InlineKeyboardButton("🔄 Yeni Viktorina", callback_data="back_to_menu")],
                    [InlineKeyboardButton("📊 Statistika", callback_data="statistics")]
                ]
                
                await query.edit_message_text(result_text, reply_markup=InlineKeyboardMarkup(keyboard))


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kömək məlumatı"""
    message = """
📖 Kömək Məlumatı

🎯 Bot Nədir?
Bu bot müxtəlif mövzularda viktorinalar təklif edir. Hər viktorinada 10 sual var və siz xal toplayırsınız.

📋 Əsas Əmrlər:
/start - Botu başlat
/quiz - Viktorina başlat
/stats - Statistikaları görün
/leaderboard - Liderboard görün
/help - Bu kömək mesajı

🎮 Oyun Qaydaları:
• Hər viktorinada 10 sual var
• Hər düzgün cavab üçün 1 xal
• Maksimum xal: 10/10
• Statistikalar avtomatik saxlanılır

💡 Məsləhət: Müxtəlif kateqoriyalarda oynayın ki, biliklərinizi genişləndirin!
    """
    await update.message.reply_text(message)


def main():
    """Botu işə salır"""
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN tapılmadı! .env faylında təyin edin.")
        return
    
    # Bot aplikasiyasını yaradır
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Əmrləri əlavə et
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("quiz", quiz))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("leaderboard", leaderboard))
    application.add_handler(CommandHandler("help", help_command))
    
    # Callback query handler
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Botu işə sal
    logger.info("Bot işə salınır...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()