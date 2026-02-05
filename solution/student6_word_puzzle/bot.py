"""
Söz Tapmacası Bot - Telegram bot əsas faylı
"""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from database import Database
from puzzle_engine import AnagramSolver, WordScramble, WordLengthPuzzle, DailyPuzzle, check_word_match
from config import BOT_TOKEN

# Logging konfiqurasiyası
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Global obyektlər
db = Database()
user_puzzles = {}  # {user_id: puzzle_data}


def get_main_menu_keyboard():
    """Əsas menyu düymələri"""
    keyboard = [
        [InlineKeyboardButton("🔤 Anagram Həlledici", callback_data="anagram_solver")],
        [InlineKeyboardButton("🎲 Anagram Tapmacası", callback_data="anagram_puzzle")],
        [InlineKeyboardButton("🔀 Söz Yarışması", callback_data="scramble")],
        [InlineKeyboardButton("📏 Söz Uzunluğu", callback_data="length_puzzle")],
        [InlineKeyboardButton("📅 Gündəlik Tapmaca", callback_data="daily_puzzle")],
        [InlineKeyboardButton("📊 Statistika", callback_data="statistics")]
    ]
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/start əmri - botu başladır"""
    user = update.effective_user
    user_id = user.id
    
    # İstifadəçini verilənlər bazasına əlavə et
    db.add_user(user_id, user.username, user.first_name)
    
    welcome_message = f"""
🧩 Söz Tapmacası Botuna Xoş Gəlmisiniz, {user.first_name}!

Bu bot ilə müxtəlif söz oyunları oynaya bilərsiniz.

✨ Xüsusiyyətlər:
• Anagram həlledici
• Anagram tapmacaları
• Söz yarışması (scramble)
• Söz uzunluğu tapmacaları
• Gündəlik tapmacalar
• Xal sistemi və statistika

📋 Əmrlər:
/start - Botu başlat
/anagram <hərflər> - Anagram həll et
/puzzle - Tapmaca oyna
/daily - Gündəlik tapmaca
/stats - Statistikaları görün
/help - Kömək

Başlamaq üçün aşağıdakı düymələrdən istifadə edin!
    """
    
    await update.message.reply_text(welcome_message, reply_markup=get_main_menu_keyboard())


async def anagram_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Anagram həlledici"""
    if not context.args:
        await update.message.reply_text(
            "🔤 Anagram Həlledici\n\n"
            "İstifadə: /anagram <hərflər>\n"
            "Məsələn: /anagram ALMA"
        )
        return
    
    letters = " ".join(context.args).upper()
    anagrams = AnagramSolver.get_anagrams(letters)
    
    if anagrams:
        text = f"🔤 '{letters}' hərflərindən tapılan sözlər:\n\n"
        for word in anagrams[:20]:  # İlk 20 söz
            text += f"• {word}\n"
        if len(anagrams) > 20:
            text += f"\n... və {len(anagrams) - 20} digər söz"
    else:
        text = f"❌ '{letters}' hərflərindən heç bir söz tapılmadı."
    
    await update.message.reply_text(text)


async def puzzle_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tapmaca başladır"""
    user_id = update.effective_user.id
    
    keyboard = [
        [InlineKeyboardButton("🎲 Anagram", callback_data="anagram_puzzle")],
        [InlineKeyboardButton("🔀 Söz Yarışması", callback_data="scramble")],
        [InlineKeyboardButton("📏 Söz Uzunluğu", callback_data="length_puzzle")],
        [InlineKeyboardButton("📅 Gündəlik", callback_data="daily_puzzle")]
    ]
    
    await update.message.reply_text(
        "🧩 Tapmaca Növü Seçin:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def daily_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gündəlik tapmaca"""
    user_id = update.effective_user.id
    
    puzzle = DailyPuzzle.generate_daily_puzzle()
    user_puzzles[user_id] = puzzle
    
    puzzle_type_names = {
        "anagram": "🔤 Anagram Tapmacası",
        "scramble": "🔀 Söz Yarışması",
        "length": "📏 Söz Uzunluğu Tapmacası"
    }
    
    text = f"""
📅 Gündəlik Tapmaca

{puzzle_type_names.get(puzzle['type'], 'Tapmaca')}

"""
    
    if puzzle['type'] == "anagram":
        text += f"🔤 Qarışdırılmış hərflər: {puzzle['scrambled']}\n\n"
    elif puzzle['type'] == "scramble":
        text += f"🔀 Qarışdırılmış söz: {puzzle['scrambled']}\n\n"
    elif puzzle['type'] == "length":
        text += f"📏 Söz: {puzzle['display']}\n\n"
    
    text += f"💡 İpucu: {puzzle.get('hint', '')}\n\n"
    text += "Cavabı yazın:"
    
    await update.message.reply_text(text)


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Statistikaları göstərir"""
    user_id = update.effective_user.id
    stats_data = db.get_statistics(user_id)
    
    if stats_data:
        puzzles_solved, puzzles_attempted, anagrams_solved, scrambles_solved, \
        length_puzzles_solved, current_streak, best_streak = stats_data
        
        success_rate = (puzzles_solved / puzzles_attempted * 100) if puzzles_attempted > 0 else 0
        
        message = f"""
📊 Sizin Statistikalarınız:

🧩 Həll edilmiş tapmacalar: {puzzles_solved}
🎯 Cəhd edilmiş tapmacalar: {puzzles_attempted}
📈 Uğur faizi: {success_rate:.1f}%

📋 Növ üzrə:
  🔤 Anagramlar: {anagrams_solved}
  🔀 Yarışmalar: {scrambles_solved}
  📏 Uzunluq: {length_puzzles_solved}

🔥 Cari seriya: {current_streak}
🏆 Ən yaxşı seriya: {best_streak}
        """
    else:
        message = "📊 Hələ heç bir tapmaca həll etməmisiniz. /puzzle ilə başlayın!"
    
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
            puzzles_solved, puzzles_attempted, anagrams_solved, scrambles_solved, \
            length_puzzles_solved, current_streak, best_streak = stats_data
            
            success_rate = (puzzles_solved / puzzles_attempted * 100) if puzzles_attempted > 0 else 0
            
            message = f"""
📊 Sizin Statistikalarınız:

🧩 Həll edilmiş: {puzzles_solved}
🎯 Cəhd edilmiş: {puzzles_attempted}
📈 Uğur faizi: {success_rate:.1f}%

📋 Növ üzrə:
  🔤 Anagramlar: {anagrams_solved}
  🔀 Yarışmalar: {scrambles_solved}
  📏 Uzunluq: {length_puzzles_solved}

🔥 Cari seriya: {current_streak}
🏆 Ən yaxşı seriya: {best_streak}
            """
        else:
            message = "📊 Hələ heç bir tapmaca həll etməmisiniz."
        
        keyboard = [[InlineKeyboardButton("🔙 Geri", callback_data="back_to_menu")]]
        await query.edit_message_text(message, reply_markup=InlineKeyboardMarkup(keyboard))
        return
    
    if data == "back_to_menu":
        await query.edit_message_text(
            "🧩 Söz Tapmacası Botu\n\nTapmaca növü seçin:",
            reply_markup=get_main_menu_keyboard()
        )
        return
    
    if data == "anagram_solver":
        await query.edit_message_text(
            "🔤 Anagram Həlledici\n\n"
            "Hərfləri yazın və bot sizə mümkün sözləri göstərəcək.\n\n"
            "İstifadə: /anagram <hərflər>\n"
            "Məsələn: /anagram ALMA"
        )
        return
    
    if data == "anagram_puzzle":
        puzzle = AnagramSolver.generate_anagram_puzzle()
        user_puzzles[user_id] = puzzle
        
        text = f"""
🔤 Anagram Tapmacası

Qarışdırılmış hərflər: {puzzle['scrambled']}

💡 İpucu: {puzzle['hint']}

Cavabı yazın:
        """
        await query.edit_message_text(text)
        return
    
    if data == "scramble":
        puzzle = WordScramble.generate_scramble()
        puzzle['type'] = 'scramble'
        user_puzzles[user_id] = puzzle
        
        text = f"""
🔀 Söz Yarışması

Qarışdırılmış söz: {puzzle['scrambled']}

💡 İpucu: {puzzle['hint']}

Cavabı yazın:
        """
        await query.edit_message_text(text)
        return
    
    if data == "length_puzzle":
        puzzle = WordLengthPuzzle.generate_puzzle()
        if puzzle:
            puzzle['type'] = 'length'
            user_puzzles[user_id] = puzzle
            
            text = f"""
📏 Söz Uzunluğu Tapmacası

Söz: {puzzle['display']}

💡 İpucu: {puzzle['hint']}

Cavabı yazın:
            """
            await query.edit_message_text(text)
        else:
            await query.answer("❌ Xəta baş verdi!", show_alert=True)
        return
    
    if data == "daily_puzzle":
        puzzle = DailyPuzzle.generate_daily_puzzle()
        user_puzzles[user_id] = puzzle
        
        puzzle_type_names = {
            "anagram": "🔤 Anagram Tapmacası",
            "scramble": "🔀 Söz Yarışması",
            "length": "📏 Söz Uzunluğu Tapmacası"
        }
        
        text = f"""
📅 Gündəlik Tapmaca

{puzzle_type_names.get(puzzle['type'], 'Tapmaca')}

"""
        
        if puzzle['type'] == "anagram":
            text += f"🔤 Qarışdırılmış hərflər: {puzzle['scrambled']}\n\n"
        elif puzzle['type'] == "scramble":
            text += f"🔀 Qarışdırılmış söz: {puzzle['scrambled']}\n\n"
        elif puzzle['type'] == "length":
            text += f"📏 Söz: {puzzle['display']}\n\n"
        
        text += f"💡 İpucu: {puzzle.get('hint', '')}\n\n"
        text += "Cavabı yazın:"
        
        await query.edit_message_text(text)
        return


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mesajları idarə edir - tapmaca cavablarını yoxlayır"""
    user_id = update.effective_user.id
    user_answer = update.message.text.strip().upper()
    
    if user_id not in user_puzzles:
        return
    
    puzzle = user_puzzles[user_id]
    correct_answer = puzzle.get('answer')
    
    if correct_answer and check_word_match(user_answer, correct_answer):
        # Düzgün cavab
        puzzle_type = puzzle.get('type', 'unknown')
        db.save_puzzle_attempt(user_id, puzzle_type, True)
        db.update_statistics(user_id, puzzle_type, True)
        
        if puzzle_type == 'daily':
            db.mark_daily_puzzle_solved(user_id)
        
        del user_puzzles[user_id]
        
        await update.message.reply_text(
            f"🎉 Təbriklər! Düzgün cavab: {correct_answer}\n\n"
            f"Yeni tapmaca üçün /puzzle yazın!",
            reply_markup=get_main_menu_keyboard()
        )
    else:
        # Səhv cavab
        puzzle_type = puzzle.get('type', 'unknown')
        db.save_puzzle_attempt(user_id, puzzle_type, False)
        db.update_statistics(user_id, puzzle_type, False)
        
        await update.message.reply_text(
            f"❌ Səhv cavab! Yenidən cəhd edin.\n\n"
            f"💡 İpucu: {puzzle.get('hint', '')}"
        )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kömək məlumatı"""
    message = """
📖 Kömək Məlumatı

🧩 Bot Nədir?
Bu bot müxtəlif söz oyunları təklif edir. Anagramlar həll edin, söz yarışmaları oynayın!

📋 Əsas Əmrlər:
/start - Botu başlat
/anagram <hərflər> - Anagram həll et
/puzzle - Tapmaca oyna
/daily - Gündəlik tapmaca
/stats - Statistikaları görün
/help - Bu kömək mesajı

🎮 Oyun Növləri:
• Anagram Həlledici - Hərflərdən sözlər tapın
• Anagram Tapmacası - Qarışdırılmış hərfləri düzəldin
• Söz Yarışması - Qarışdırılmış sözü tapın
• Söz Uzunluğu - Verilən hərflərdən söz tapın
• Gündəlik Tapmaca - Hər gün yeni tapmaca

💡 Məsləhət: Azərbaycan dilində sözlər istifadə olunur!
    """
    await update.message.reply_text(message, reply_markup=get_main_menu_keyboard())


def main():
    """Botu işə salır"""
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN tapılmadı! .env faylında təyin edin.")
        return
    
    # Bot aplikasiyasını yaradır
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Əmrləri əlavə et
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("anagram", anagram_command))
    application.add_handler(CommandHandler("puzzle", puzzle_command))
    application.add_handler(CommandHandler("daily", daily_command))
    application.add_handler(CommandHandler("stats", stats))
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