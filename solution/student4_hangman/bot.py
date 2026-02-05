"""
Adam Asma Oyunu Bot - Telegram bot əsas faylı
"""
import logging
import string
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from database import Database
from game_logic import HangmanGame
from word_database import get_word, get_categories, get_difficulties
from config import BOT_TOKEN

# Logging konfiqurasiyası
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Global obyektlər
db = Database()
user_games = {}  # {user_id: HangmanGame instance}
user_game_info = {}  # {user_id: {"difficulty": ..., "category": ...}}

# Azərbaycan əlifbası
AZERBAIJAN_ALPHABET = "ABCÇDEƏFGĞHXIİJKQLMNOÖPRSŞTUÜVYZ"


def get_difficulty_keyboard():
    """Çətinlik səviyyəsi seçimi üçün düymələr"""
    difficulties = get_difficulties()
    keyboard = []
    
    emoji_map = {"asan": "🟢", "orta": "🟡", "çətin": "🔴"}
    
    for diff in difficulties:
        emoji = emoji_map.get(diff, "📝")
        keyboard.append([InlineKeyboardButton(
            f"{emoji} {diff.capitalize()}",
            callback_data=f"difficulty_{diff}"
        )])
    
    keyboard.append([InlineKeyboardButton("📊 Statistika", callback_data="statistics")])
    
    return InlineKeyboardMarkup(keyboard)


def get_category_keyboard(difficulty):
    """Kateqoriya seçimi üçün düymələr"""
    categories = get_categories(difficulty)
    keyboard = []
    
    for i in range(0, len(categories), 2):
        row = []
        cat1 = categories[i]
        row.append(InlineKeyboardButton(
            cat1.capitalize(),
            callback_data=f"category_{difficulty}_{cat1}"
        ))
        
        if i + 1 < len(categories):
            cat2 = categories[i + 1]
            row.append(InlineKeyboardButton(
                cat2.capitalize(),
                callback_data=f"category_{difficulty}_{cat2}"
            ))
        keyboard.append(row)
    
    keyboard.append([InlineKeyboardButton("🔙 Geri", callback_data="back_to_difficulty")])
    
    return InlineKeyboardMarkup(keyboard)


def get_letter_keyboard(game):
    """Hərf seçimi üçün düymələr"""
    keyboard = []
    guessed = set(game.guessed_letters)
    
    # Azərbaycan əlifbasından hərflər
    letters = list(AZERBAIJAN_ALPHABET)
    
    row = []
    for letter in letters:
        if letter in guessed:
            # Artıq təxmin edilmiş hərflər
            row.append(InlineKeyboardButton(f"❌ {letter}", callback_data=f"letter_used_{letter}"))
        else:
            row.append(InlineKeyboardButton(letter, callback_data=f"letter_{letter}"))
        
        if len(row) == 6:  # Hər sətirdə 6 hərf
            keyboard.append(row)
            row = []
    
    if row:
        keyboard.append(row)
    
    keyboard.append([InlineKeyboardButton("🔄 Yeni Oyun", callback_data="new_game")])
    keyboard.append([InlineKeyboardButton("📊 Statistika", callback_data="statistics")])
    
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/start əmri - botu başladır"""
    user = update.effective_user
    user_id = user.id
    
    # İstifadəçini verilənlər bazasına əlavə et
    db.add_user(user_id, user.username, user.first_name)
    
    welcome_message = f"""
🎮 Adam Asma Oyunu Botuna Xoş Gəlmisiniz, {user.first_name}!

Bu bot ilə klassik Adam Asma oyununu oynaya bilərsiniz.

✨ Xüsusiyyətlər:
• Müxtəlif çətinlik səviyyələri (asan, orta, çətin)
• Müxtəlif kateqoriyalar (heyvanlar, şəhərlər, meyvələr, idman)
• Vizual oyun göstəricisi
• Xal sistemi və statistika

📋 Əmrlər:
/start - Botu başlat
/newgame - Yeni oyun başlat
/stats - Statistikaları görün
/help - Kömək

Başlamaq üçün /newgame yazın!
    """
    
    await update.message.reply_text(welcome_message)


async def new_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Yeni oyun başladır"""
    user_id = update.effective_user.id
    
    # Köhnə oyunu sil
    if user_id in user_games:
        del user_games[user_id]
    if user_id in user_game_info:
        del user_game_info[user_id]
    
    message = "🎮 Çətinlik Səviyyəsi Seçin:\n\nAşağıdakı səviyyələrdən birini seçin:"
    await update.message.reply_text(message, reply_markup=get_difficulty_keyboard())


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Statistikaları göstərir"""
    user_id = update.effective_user.id
    stats_data = db.get_statistics(user_id)
    
    if stats_data:
        games_played, games_won, games_lost, total_wrong_guesses, current_streak, best_streak = stats_data
        win_rate = (games_won / games_played * 100) if games_played > 0 else 0
        avg_wrong = (total_wrong_guesses / games_played) if games_played > 0 else 0
        
        message = f"""
📊 Sizin Statistikalarınız:

🎮 Oynanılan oyunlar: {games_played}
✅ Qalibiyyətlər: {games_won}
❌ Məğlubiyyətlər: {games_lost}
📈 Qalibiyyət faizi: {win_rate:.1f}%
🔥 Cari seriya: {current_streak}
🏆 Ən yaxşı seriya: {best_streak}
📉 Orta səhv sayı: {avg_wrong:.1f}
        """
    else:
        message = "📊 Hələ heç bir oyun oynamamısınız. /newgame ilə başlayın!"
    
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
            games_played, games_won, games_lost, total_wrong_guesses, current_streak, best_streak = stats_data
            win_rate = (games_won / games_played * 100) if games_played > 0 else 0
            avg_wrong = (total_wrong_guesses / games_played) if games_played > 0 else 0
            
            message = f"""
📊 Sizin Statistikalarınız:

🎮 Oynanılan oyunlar: {games_played}
✅ Qalibiyyətlər: {games_won}
❌ Məğlubiyyətlər: {games_lost}
📈 Qalibiyyət faizi: {win_rate:.1f}%
🔥 Cari seriya: {current_streak}
🏆 Ən yaxşı seriya: {best_streak}
📉 Orta səhv sayı: {avg_wrong:.1f}
            """
        else:
            message = "📊 Hələ heç bir oyun oynamamısınız."
        
        keyboard = [[InlineKeyboardButton("🔙 Geri", callback_data="back_to_menu")]]
        await query.edit_message_text(message, reply_markup=InlineKeyboardMarkup(keyboard))
        return
    
    if data == "back_to_menu" or data == "new_game":
        # Yeni oyun
        if user_id in user_games:
            del user_games[user_id]
        if user_id in user_game_info:
            del user_game_info[user_id]
        
        message = "🎮 Çətinlik Səviyyəsi Seçin:\n\nAşağıdakı səviyyələrdən birini seçin:"
        await query.edit_message_text(message, reply_markup=get_difficulty_keyboard())
        return
    
    if data == "back_to_difficulty":
        message = "🎮 Çətinlik Səviyyəsi Seçin:\n\nAşağıdakı səviyyələrdən birini seçin:"
        await query.edit_message_text(message, reply_markup=get_difficulty_keyboard())
        return
    
    if data.startswith("difficulty_"):
        # Çətinlik seçildi
        difficulty = data.replace("difficulty_", "")
        user_game_info[user_id] = {"difficulty": difficulty}
        
        message = f"📚 Kateqoriya Seçin ({difficulty.capitalize()}):\n\nAşağıdakı kateqoriyalardan birini seçin:"
        await query.edit_message_text(message, reply_markup=get_category_keyboard(difficulty))
        return
    
    if data.startswith("category_"):
        # Kateqoriya seçildi
        parts = data.replace("category_", "").split("_")
        difficulty = parts[0]
        category = "_".join(parts[1:])
        
        # Söz seç
        word = get_word(difficulty, category)
        game = HangmanGame(word)
        user_games[user_id] = game
        user_game_info[user_id] = {"difficulty": difficulty, "category": category}
        
        status = game.get_status()
        hangman_display = game.get_hangman_display()
        
        message = f"""
🎮 Oyun Başladı!

📚 Kateqoriya: {category.capitalize()}
🎯 Çətinlik: {difficulty.capitalize()}

{hangman_display}

Söz: {status['display_word']}

Təxmin edilmiş hərflər: {', '.join(status['guessed_letters']) if status['guessed_letters'] else 'Yoxdur'}

Hərf seçin:
        """
        
        await query.edit_message_text(message, reply_markup=get_letter_keyboard(game))
        return
    
    if data.startswith("letter_"):
        # Hərf seçildi
        if user_id not in user_games:
            await query.answer("❌ Aktiv oyun yoxdur! Yeni oyun başladın.", show_alert=True)
            return
        
        letter = data.replace("letter_", "").replace("letter_used_", "")
        game = user_games[user_id]
        
        result = game.guess_letter(letter)
        
        status = game.get_status()
        hangman_display = game.get_hangman_display()
        
        game_info = user_game_info.get(user_id, {})
        category = game_info.get("category", "naməlum")
        difficulty = game_info.get("difficulty", "naməlum")
        
        if result["status"] == "won":
            # Qalib
            db.save_game(user_id, game.word, difficulty, category, True, game.wrong_guesses)
            db.update_statistics(user_id, True, game.wrong_guesses)
            del user_games[user_id]
            del user_game_info[user_id]
            
            message = f"""
🎉 {result['message']}

{hangman_display}

Söz: {status['display_word']}

Yeni oyun başlatmaq istəyirsiniz?
            """
            keyboard = [[InlineKeyboardButton("🔄 Yeni Oyun", callback_data="new_game")]]
            await query.edit_message_text(message, reply_markup=InlineKeyboardMarkup(keyboard))
            return
        
        if result["status"] == "lost":
            # Məğlub
            db.save_game(user_id, game.word, difficulty, category, False, game.wrong_guesses)
            db.update_statistics(user_id, False, game.wrong_guesses)
            del user_games[user_id]
            del user_game_info[user_id]
            
            message = f"""
{result['message']}

{hangman_display}

Yeni oyun başlatmaq istəyirsiniz?
            """
            keyboard = [[InlineKeyboardButton("🔄 Yeni Oyun", callback_data="new_game")]]
            await query.edit_message_text(message, reply_markup=InlineKeyboardMarkup(keyboard))
            return
        
        # Oyun davam edir
        message = f"""
🎮 Oyun Davam Edir

📚 Kateqoriya: {category.capitalize()}
🎯 Çətinlik: {difficulty.capitalize()}

{hangman_display}

Söz: {status['display_word']}

Təxmin edilmiş hərflər: {', '.join(status['guessed_letters']) if status['guessed_letters'] else 'Yoxdur'}

{result['message']}
Qalan cəhd: {status['max_wrong'] - status['wrong_guesses']}

Hərf seçin:
        """
        
        await query.edit_message_text(message, reply_markup=get_letter_keyboard(game))
        
        if result["status"] == "wrong":
            await query.answer(result["message"], show_alert=True)
        elif result["status"] == "correct":
            await query.answer(result["message"], show_alert=True)
    
    if data.startswith("letter_used_"):
        await query.answer("ℹ️ Bu hərfi artıq təxmin etmisiniz!", show_alert=True)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kömək məlumatı"""
    message = """
📖 Kömək Məlumatı

🎮 Oyun Qaydaları:
• Sözü təxmin etmək üçün hərflər seçin
• Hər səhv hərf üçün adamın bir hissəsi çəkilir
• 6 səhv hərfdən sonra oyun bitir
• Sözü tam taparsanız qalib gəlirsiniz

📋 Əmrlər:
/start - Botu başlat
/newgame - Yeni oyun başlat
/stats - Statistikaları görün
/help - Bu kömək mesajı

💡 Məsləhət: Azərbaycan əlifbasından hərflər seçin!
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
    application.add_handler(CommandHandler("newgame", new_game))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("help", help_command))
    
    # Callback query handler
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Botu işə sal
    logger.info("Bot işə salınır...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()