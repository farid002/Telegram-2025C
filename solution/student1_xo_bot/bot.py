"""
X-O Oyun Botu - Telegram bot əsas faylı
"""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from game_logic import TicTacToe
from database import Database
from config import BOT_TOKEN

# Logging konfiqurasiyası
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Global obyektlər
db = Database()
user_games = {}  # {user_id: TicTacToe instance}


def get_keyboard_from_board(game):
    """Oyun taxtasından inline keyboard yaradır"""
    keyboard = []
    for i in range(3):
        row = []
        for j in range(3):
            cell_value = game.board[i][j]
            if cell_value == ' ':
                # Boş xanalar üçün düymə - hərəkət etmək üçün
                button_text = f"{i*3 + j + 1}"
                callback_data = f"move_{i}_{j}"
            else:
                # Dolu xanalar üçün düymə yoxdur
                button_text = " " if cell_value == 'X' else " "
                callback_data = f"empty_{i}_{j}"
            row.append(InlineKeyboardButton(button_text, callback_data=callback_data))
        keyboard.append(row)
    
    # Əlavə düymələr
    keyboard.append([
        InlineKeyboardButton("🔄 Yeni Oyun", callback_data="new_game"),
        InlineKeyboardButton("📊 Statistika", callback_data="statistics")
    ])
    
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/start əmri - botu başladır"""
    user = update.effective_user
    user_id = user.id
    
    # İstifadəçini verilənlər bazasına əlavə et
    db.add_user(user_id, user.username, user.first_name)
    
    welcome_message = f"""
🎮 X-O Oyun Botuna Xoş Gəlmisiniz, {user.first_name}!

Bu bot ilə mənimlə X-O oynaya bilərsiniz.

📋 Əmrlər:
/start - Botu başlat
/newgame - Yeni oyun başlat
/stats - Statistikalarınızı görün
/help - Kömək

Başlamaq üçün /newgame yazın və ya aşağıdakı düyməni basın!
    """
    
    keyboard = [[InlineKeyboardButton("🎮 Yeni Oyun Başlat", callback_data="new_game")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)


async def new_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Yeni oyun başladır"""
    user_id = update.effective_user.id
    
    # Yeni oyun yaradır
    game = TicTacToe()
    user_games[user_id] = game
    
    message = f"""
🎮 Yeni Oyun Başladı!

Siz ❌ ilə oynayırsınız
Mən ⭕ ilə oynayıram

{game.get_board_display()}

Sizin hərəkətiniz! Aşağıdakı düymələrdən birini seçin.
    """
    
    keyboard = get_keyboard_from_board(game)
    await update.message.reply_text(message, reply_markup=keyboard)


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Düymə basılmalarını idarə edir"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    data = query.data
    
    if data == "new_game":
        # Yeni oyun
        game = TicTacToe()
        user_games[user_id] = game
        
        message = f"""
🎮 Yeni Oyun Başladı!

Siz ❌ ilə oynayırsınız
Mən ⭕ ilə oynayıram

{game.get_board_display()}

Sizin hərəkətiniz!
        """
        keyboard = get_keyboard_from_board(game)
        await query.edit_message_text(message, reply_markup=keyboard)
        return
    
    if data == "statistics":
        # Statistika göstər
        stats = db.get_statistics(user_id)
        if stats:
            games_played, games_won, games_lost, games_draw, win_streak, best_streak = stats
            win_rate = (games_won / games_played * 100) if games_played > 0 else 0
            
            message = f"""
📊 Sizin Statistikalarınız:

🎮 Oynanılan oyunlar: {games_played}
✅ Qalibiyyətlər: {games_won}
❌ Məğlubiyyətlər: {games_lost}
🤝 Heç-heçə: {games_draw}
📈 Qalibiyyət faizi: {win_rate:.1f}%
🔥 Cari seriya: {win_streak}
🏆 Ən yaxşı seriya: {best_streak}
            """
        else:
            message = "📊 Hələ heç bir oyun oynamamısınız. /newgame ilə başlayın!"
        
        keyboard = [[InlineKeyboardButton("🔙 Geri", callback_data="back_to_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(message, reply_markup=reply_markup)
        return
    
    if data == "back_to_menu":
        # Ana menyuya qayıt
        message = """
🎮 X-O Oyun Botu

Yeni oyun başlatmaq üçün düyməni basın!
        """
        keyboard = [[InlineKeyboardButton("🎮 Yeni Oyun Başlat", callback_data="new_game")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(message, reply_markup=reply_markup)
        return
    
    # Hərəkət etmə
    if data.startswith("move_"):
        if user_id not in user_games:
            await query.answer("❌ Aktiv oyun yoxdur! Yeni oyun başladın.", show_alert=True)
            return
        
        game = user_games[user_id]
        _, row, col = data.split("_")
        row, col = int(row), int(col)
        
        # İstifadəçi hərəkəti
        if not game.make_move(row, col, 'X'):
            await query.answer("❌ Bu xana artıq doldurulub!", show_alert=True)
            return
        
        # Oyun vəziyyətini yoxla
        game_state = game.get_game_state()
        
        if game_state == 'win':
            # İstifadəçi qalib
            db.save_game(user_id, 'win', game.moves_count)
            db.update_statistics(user_id, 'win')
            del user_games[user_id]
            
            message = f"""
🎉 Təbriklər! Siz qalib gəldiniz! 🎉

{game.get_board_display()}

Yeni oyun başlatmaq istəyirsiniz?
            """
            keyboard = [[InlineKeyboardButton("🎮 Yeni Oyun", callback_data="new_game")]]
            await query.edit_message_text(message, reply_markup=InlineKeyboardMarkup(keyboard))
            return
        
        if game_state == 'draw':
            # Heç-heçə
            db.save_game(user_id, 'draw', game.moves_count)
            db.update_statistics(user_id, 'draw')
            del user_games[user_id]
            
            message = f"""
🤝 Heç-heçə! Heç kim qalib gəlmədi.

{game.get_board_display()}

Yeni oyun başlatmaq istəyirsiniz?
            """
            keyboard = [[InlineKeyboardButton("🎮 Yeni Oyun", callback_data="new_game")]]
            await query.edit_message_text(message, reply_markup=InlineKeyboardMarkup(keyboard))
            return
        
        # Bot hərəkəti
        bot_move = game.get_best_move()
        if bot_move:
            game.make_move(bot_move[0], bot_move[1], 'O')
            game_state = game.get_game_state()
            
            if game_state == 'lose':
                # Bot qalib
                db.save_game(user_id, 'lose', game.moves_count)
                db.update_statistics(user_id, 'lose')
                del user_games[user_id]
                
                message = f"""
😔 Təəssüf! Mən qalib gəldim! 😄

{game.get_board_display()}

Yeni oyun başlatmaq istəyirsiniz?
                """
                keyboard = [[InlineKeyboardButton("🎮 Yeni Oyun", callback_data="new_game")]]
                await query.edit_message_text(message, reply_markup=InlineKeyboardMarkup(keyboard))
                return
            
            if game_state == 'draw':
                # Heç-heçə
                db.save_game(user_id, 'draw', game.moves_count)
                db.update_statistics(user_id, 'draw')
                del user_games[user_id]
                
                message = f"""
🤝 Heç-heçə! Heç kim qalib gəlmədi.

{game.get_board_display()}

Yeni oyun başlatmaq istəyirsiniz?
                """
                keyboard = [[InlineKeyboardButton("🎮 Yeni Oyun", callback_data="new_game")]]
                await query.edit_message_text(message, reply_markup=InlineKeyboardMarkup(keyboard))
                return
        
        # Oyun davam edir
        message = f"""
🎮 Oyun Davam Edir

{game.get_board_display()}

Sizin hərəkətiniz!
        """
        keyboard = get_keyboard_from_board(game)
        await query.edit_message_text(message, reply_markup=keyboard)


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Statistikaları göstərir"""
    user_id = update.effective_user.id
    stats = db.get_statistics(user_id)
    
    if stats:
        games_played, games_won, games_lost, games_draw, win_streak, best_streak = stats
        win_rate = (games_won / games_played * 100) if games_played > 0 else 0
        
        message = f"""
📊 Sizin Statistikalarınız:

🎮 Oynanılan oyunlar: {games_played}
✅ Qalibiyyətlər: {games_won}
❌ Məğlubiyyətlər: {games_lost}
🤝 Heç-heçə: {games_draw}
📈 Qalibiyyət faizi: {win_rate:.1f}%
🔥 Cari seriya: {win_streak}
🏆 Ən yaxşı seriya: {best_streak}
        """
    else:
        message = "📊 Hələ heç bir oyun oynamamısınız. /newgame ilə başlayın!"
    
    await update.message.reply_text(message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kömək məlumatı"""
    message = """
📖 Kömək Məlumatı

🎮 Oyun Qaydaları:
• Siz ❌ ilə oynayırsınız
• Mən ⭕ ilə oynayıram
• İlk 3 xananı dolduran qalib gəlir
• Sətir, sütun və ya diaqonal üzrə

📋 Əmrlər:
/start - Botu başlat
/newgame - Yeni oyun başlat
/stats - Statistikalarınızı görün
/help - Bu kömək mesajı

🎯 Məqsəd: 3 xananı ardıcıl doldurmaq!
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