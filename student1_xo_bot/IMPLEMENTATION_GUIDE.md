# X-O Oyun Botu - İmplementasiya Təlimatı

Bu təlimat sizə X-O (Tic-Tac-Toe) oyun botunu addım-addım hazırlamağa kömək edəcək. Cursor AI-dan istifadə edərək hər addımı tamamlayın.

## Giriş

Bu layihədə Telegram üzərində X-O oyunu oynaya biləcəyiniz bot hazırlayacaqsınız. Bot AI rəqib ilə oynayacaq və oyun statistikalarınızı izləyəcək.

### Nə qurulacaq?

1. **Telegram Bot** - İstifadəçilərlə qarşılıqlı əlaqə
2. **Oyun Məntiqi** - X-O oyununun qaydaları və vəziyyət idarəetməsi
3. **AI Rəqib** - Minimax alqoritmi ilə güclü rəqib
4. **Verilənlər Bazası** - Oyun tarixçəsi və statistika

### Texnologiyalar

- Python 3.8+
- python-telegram-bot (v20+)
- SQLite3
- python-dotenv

---

## Addım 1: Konfiqurasiya (config.py)

### Nə üçün lazımdır?

`config.py` faylı botun konfiqurasiya məlumatlarını saxlayır. Bu fayl bot token-i və digər parametrləri təyin edir.

### Cursor AI-dan kömək almaq

Cursor AI-ya belə deyin:
> "Mənə config.py faylı yarat. Bu fayl python-dotenv istifadə edərək .env faylından BOT_TOKEN oxumalıdır. Həmçinin DATABASE_FILE və LOG_LEVEL parametrləri olmalıdır."

### Nə yazılmalıdır?

1. **Import-lar:**
   - `os` - Sistem dəyişənlərini oxumaq üçün
   - `dotenv` - .env faylından dəyərləri oxumaq üçün

2. **Dəyişənlər:**
   - `BOT_TOKEN` - Telegram bot token-i (.env-dən)
   - `DATABASE_FILE` - Verilənlər bazası fayl adı
   - `LOG_LEVEL` - Logging səviyyəsi

### Nümunə strukturu:

```python
"""
Konfiqurasiya faylı - Bot token və digər parametrlər
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Token (BotFather-dən alınır)
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# Verilənlər bazası faylı
DATABASE_FILE = "xo_bot.db"

# Logging konfiqurasiyası
LOG_LEVEL = "INFO"
```

### Yoxlama

Fayl yaradıldıqdan sonra `.env` faylında `BOT_TOKEN` olduğundan əmin olun.

---

## Addım 2: Verilənlər Bazası (database.py)

### Nə üçün lazımdır?

Verilənlər bazası istifadəçi məlumatlarını, oyun tarixçəsini və statistikaları saxlayır.

### Cursor AI-dan kömək almaq

Cursor AI-ya belə deyin:
> "Mənə database.py faylı yarat. SQLite istifadə edərək 3 cədvəl lazımdır: users (user_id, username, first_name), games (game_id, user_id, result, moves_count), statistics (user_id, games_played, games_won, games_lost, games_draw, win_streak, best_streak). Database sinfi yarat və init_database, add_user, save_game, update_statistics, get_statistics funksiyaları əlavə et."

### Verilənlər Bazası Strukturu

**1. users cədvəli:**
- `user_id` (PRIMARY KEY) - Telegram istifadəçi ID
- `username` - İstifadəçi adı
- `first_name` - Ad
- `created_at` - Yaradılma tarixi

**2. games cədvəli:**
- `game_id` (PRIMARY KEY, AUTOINCREMENT)
- `user_id` (FOREIGN KEY) - İstifadəçi ID
- `result` - Nəticə (win/lose/draw)
- `moves_count` - Hərəkət sayı
- `created_at` - Tarix

**3. statistics cədvəli:**
- `user_id` (PRIMARY KEY)
- `games_played` - Oynanılan oyunlar
- `games_won` - Qalibiyyətlər
- `games_lost` - Məğlubiyyətlər
- `games_draw` - Heç-heçə
- `win_streak` - Cari seriya
- `best_streak` - Ən yaxşı seriya

### Funksiyalar

1. **`__init__(self)`** - Verilənlər bazasını yaradır və cədvəlləri hazırlayır
2. **`init_database(self)`** - Cədvəlləri yaradır (CREATE TABLE IF NOT EXISTS)
3. **`add_user(self, user_id, username, first_name)`** - Yeni istifadəçi əlavə edir
4. **`save_game(self, user_id, result, moves_count)`** - Oyun nəticəsini saxlayır
5. **`update_statistics(self, user_id, result)`** - Statistikaları yeniləyir
6. **`get_statistics(self, user_id)`** - İstifadəçi statistikalarını qaytarır

### SQL Nümunələri

```sql
-- users cədvəli
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

-- games cədvəli
CREATE TABLE IF NOT EXISTS games (
    game_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    result TEXT,
    moves_count INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
```

### Yoxlama

Fayl yaradıldıqdan sonra verilənlər bazası faylının yaradıldığını yoxlayın.

---

## Addım 3: Oyun Məntiqi (game_logic.py)

### Nə üçün lazımdır?

`game_logic.py` faylı oyunun bütün məntiqini ehtiva edir: taxta vəziyyəti, qalibiyyət yoxlama, AI hərəkəti.

### Cursor AI-dan kömək almaq

Cursor AI-ya belə deyin:
> "Mənə game_logic.py faylı yarat. TicTacToe sinfi lazımdır. Oyun taxtası 3x3 list olmalıdır. make_move, check_winner, is_board_full, get_best_move funksiyaları lazımdır. get_best_move funksiyası minimax alqoritmi istifadə etməlidir."

### TicTacToe Sinfi

**Əsas atributlar:**
- `board` - 3x3 oyun taxtası (list of lists)
- `current_player` - Cari oyunçu ('X' və ya 'O')
- `moves_count` - Hərəkət sayı

**Funksiyalar:**

1. **`__init__(self)`** - Boş taxta ilə oyunu başladır
2. **`get_board_display(self)`** - Taxtanı emoji ilə gözəl formada göstərir
3. **`make_move(self, row, col, player)`** - Hərəkət edir
4. **`check_winner(self)`** - Qalibiyyəti yoxlayır (sətir, sütun, diaqonal)
5. **`is_board_full(self)`** - Taxta dolu olub olmadığını yoxlayır
6. **`get_game_state(self)`** - Oyun vəziyyətini qaytarır (win/lose/draw/playing)
7. **`get_available_moves(self)`** - Mövcud hərəkətləri qaytarır
8. **`minimax(self, depth, is_maximizing)`** - Minimax alqoritmi
9. **`get_best_move(self)`** - AI üçün ən yaxşı hərəkəti tapır

### Minimax Alqoritmi İzahı

Minimax oyun nəzəriyyəsində istifadə olunan alqoritmdir:

1. **Məqsəd:** Bot üçün ən yaxşı hərəkəti tapmaq
2. **Prinsip:** Bütün mümkün oyun vəziyyətlərini yoxlayır
3. **Hesablama:**
   - Bot qalib gələrsə: +10 xal
   - İstifadəçi qalib gələrsə: -10 xal
   - Heç-heçə: 0 xal
4. **Rekursiya:** Hər hərəkət üçün rekursiv olaraq nəticəni hesablayır

### Nümunə Kod Strukturu

```python
class TicTacToe:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.moves_count = 0
    
    def check_winner(self):
        # Sətirləri yoxla
        for row in self.board:
            if row[0] == row[1] == row[2] != ' ':
                return row[0]
        # ... sütunlar və diaqonallar
```

### Yoxlama

Oyun məntiqini test edin - taxta yaratma, hərəkət etmə, qalibiyyət yoxlama.

---

## Addım 4: Telegram Bot (bot.py)

### Nə üçün lazımdır?

`bot.py` faylı botun əsas faylıdır. Burada Telegram API ilə qarşılıqlı əlaqə qurulur.

### Cursor AI-dan kömək almaq

Cursor AI-ya belə deyin:
> "Mənə bot.py faylı yarat. python-telegram-bot v20 istifadə et. /start, /newgame, /stats, /help əmrləri lazımdır. Inline keyboard buttons ilə oyun taxtası göstərməliyəm. Callback query handler ilə düymə basılmalarını idarə etməliyəm."

### Bot Strukturu

**1. Import-lar:**
```python
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
```

**2. Handler-lər:**
- `start()` - /start əmri
- `new_game()` - /newgame əmri
- `stats()` - /stats əmri
- `button_callback()` - Düymə basılmaları
- `help_command()` - /help əmri

**3. Global obyektlər:**
- `db` - Database instance
- `user_games` - {user_id: TicTacToe instance} - Aktiv oyunlar

### Inline Keyboard Yaratma

Oyun taxtası üçün düymələr:

```python
def get_keyboard_from_board(game):
    keyboard = []
    for i in range(3):
        row = []
        for j in range(3):
            if game.board[i][j] == ' ':
                button_text = f"{i*3 + j + 1}"
                callback_data = f"move_{i}_{j}"
            else:
                # Dolu xana
                button_text = " " 
                callback_data = f"empty_{i}_{j}"
            row.append(InlineKeyboardButton(button_text, callback_data=callback_data))
        keyboard.append(row)
    return InlineKeyboardMarkup(keyboard)
```

### Oyun Axını

1. İstifadəçi `/newgame` yazır
2. Yeni `TicTacToe` instance yaradılır
3. Taxta düymələrlə göstərilir
4. İstifadəçi düyməyə basır
5. Hərəkət edilir, vəziyyət yoxlanılır
6. Bot hərəkət edir (Minimax ilə)
7. Oyun bitərsə, statistika yenilənir

### Mesaj Formatlaşdırması

Emoji istifadə edin:
- ❌ - İstifadəçi (X)
- ⭕ - Bot (O)
- ⬜ - Boş xana

### Yoxlama

Botu işə salın və test edin:
1. `/start` yazın
2. Yeni oyun başladın
3. Düymələrə basın
4. Oyunun işlədiyini yoxlayın

---

## Addım 5: Test və Debugging

### Test Etmə

1. **Oyun məntiqini test edin:**
   ```python
   game = TicTacToe()
   game.make_move(0, 0, 'X')
   assert game.check_winner() is None
   ```

2. **Verilənlər bazasını test edin:**
   ```python
   db = Database()
   db.add_user(123, "test_user")
   stats = db.get_statistics(123)
   ```

3. **Botu test edin:**
   - Bütün əmrləri sınayın
   - Düymələrin işlədiyini yoxlayın
   - Oyunun düzgün işlədiyini yoxlayın

### Ümumi Problemlər

**Problem:** Bot işə salınmır
- **Həll:** `.env` faylında `BOT_TOKEN` düzgün yazılıbmı yoxlayın

**Problem:** Düymələr işləmir
- **Həll:** Callback query handler düzgün qeydiyyatdan keçibmi?

**Problem:** Verilənlər bazası xətası
- **Həll:** Python-un yazma icazəsi varmı? Fayl yaradıla bilirmi?

**Problem:** Minimax çox yavaş işləyir
- **Həll:** Bu normaldır, amma praktikada çox sürətlidir (3x3 taxta)

### Debugging Məsləhətləri

1. **Logging istifadə edin:**
   ```python
   import logging
   logging.basicConfig(level=logging.INFO)
   logger = logging.getLogger(__name__)
   logger.info("Mesaj")
   ```

2. **Print istifadə edin:**
   ```python
   print(f"Debug: {variable}")
   ```

3. **Try-except blokları:**
   ```python
   try:
       # kod
   except Exception as e:
       logger.error(f"Xəta: {e}")
   ```

---

## Cursor AI İstifadəsi

### Tövsiyə Olunan Promptlar

1. **Fayl yaratmaq üçün:**
   > "Mənə config.py faylı yarat. python-dotenv istifadə edərək .env faylından BOT_TOKEN oxumalıdır."

2. **Funksiya yazmaq üçün:**
   > "Mənə check_winner funksiyası yaz. Bu funksiya 3x3 taxtada qalibiyyəti yoxlamalıdır - sətir, sütun və diaqonal üzrə."

3. **Alqoritm üçün:**
   > "Mənə minimax alqoritmi yaz. Bu alqoritm Tic-Tac-Toe oyunu üçün ən yaxşı hərəkəti tapmalıdır."

4. **Debugging üçün:**
   > "Bu kodda xəta var. Xəta mesajı: [xəta]. Nə səhvdir?"

### Cursor AI ilə İşləmə Strategiyası

1. **Kiçik addımlarla işləyin:**
   - Əvvəlcə config.py yaradın
   - Sonra database.py
   - Sonra game_logic.py
   - Nəhayət bot.py

2. **Hər addımı test edin:**
   - Hər fayl yaradıldıqdan sonra test edin
   - Xəta varsa, düzəldin

3. **Sual verin:**
   - Anlaşılmaz bir şey varsa, Cursor AI-dan soruşun
   - Kod nümunələri istəyin

4. **Kod izahı istəyin:**
   > "Bu kodun nə etdiyini izah et"

---

## Tövsiyə Olunan İş Sırası

1. ✅ `config.py` yaradın və test edin
2. ✅ `database.py` yaradın, cədvəlləri yoxlayın
3. ✅ `game_logic.py` yaradın, oyun məntiqini test edin
4. ✅ `bot.py` yaradın, əmrləri test edin
5. ✅ Bütün funksiyaları birləşdirin
6. ✅ Tam test edin

---

## Əlavə Məsləhətlər

1. **Kod təmizliyi:**
   - Funksiyaları kiçik saxlayın
   - Dəyişən adları aydın olsun
   - Kommentlər əlavə edin

2. **Error handling:**
   - Try-except blokları istifadə edin
   - İstifadəçiyə aydın xəta mesajları göstərin

3. **User experience:**
   - Emoji istifadə edin
   - Aydın mesajlar yazın
   - Düymələr rahat olsun

4. **Performans:**
   - Minimax alqoritmi praktikada çox sürətlidir
   - Verilənlər bazası sorğuları sürətli olmalıdır

---

## Növbəti Addımlar

Layihəni tamamladıqdan sonra:

1. Botu test edin
2. Statistikaları yoxlayın
3. AI-nın düzgün işlədiyini yoxlayın
4. Kodunuzu təmizləyin
5. Dokumentasiya əlavə edin

Uğurlar! 🎮