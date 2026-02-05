# Adam Asma Oyunu Bot - İmplementasiya Təlimatı

Bu təlimat sizə klassik Adam Asma oyununu Telegram üzərində oynaya biləcəyiniz botu addım-addım hazırlamağa kömək edəcək.

## Giriş

Bu layihədə klassik Adam Asma oyununu Telegram üzərində oynaya biləcəyiniz bot hazırlayacaqsınız. Bot müxtəlif çətinlik səviyyələri və kateqoriyalar təklif edəcək.

### Nə qurulacaq?

1. **Söz Bazası** - Müxtəlif çətinlik səviyyələrində sözlər
2. **Oyun Məntiqi** - Hərf təxmin etmə və qalibiyyət yoxlama
3. **Vizual Göstərici** - Adamın vəziyyətini göstərmə
4. **Çətinlik Səviyyələri** - Asan, orta, çətin
5. **Statistika** - Oyun nəticələri

### Texnologiyalar

- Python 3.8+
- python-telegram-bot (v20+)
- SQLite3
- python-dotenv

---

## Addım 1: Konfiqurasiya (config.py)

### Nə üçün lazımdır?

Bot token-i və oyun parametrlərini saxlayır.

### Cursor AI-dan kömək almaq

> "Mənə config.py faylı yarat. BOT_TOKEN, DATABASE_FILE və MAX_WRONG_GUESSES (maksimum səhv hərf sayı, məsələn 6) parametrləri lazımdır."

---

## Addım 2: Söz Bazası (word_database.py)

### Nə üçün lazımdır?

Müxtəlif çətinlik səviyyələrində sözləri saxlayır.

### Cursor AI-dan kömək almaq

> "Mənə word_database.py faylı yarat. WORDS_DATABASE sözlük strukturu lazımdır: {'asan': {'heyvanlar': [...], 'şəhərlər': [...]}, 'orta': {...}, 'çətin': {...}}. get_word(difficulty, category) funksiyası təsadüfi söz qaytarmalıdır."

### Söz Bazası Strukturu

```python
WORDS_DATABASE = {
    "asan": {
        "heyvanlar": ["it", "pişik", "at", ...],
        "şəhərlər": ["bakı", "gəncə", ...],
        "meyvələr": ["alma", "armud", ...]
    },
    "orta": {...},
    "çətin": {...}
}
```

### Funksiyalar

1. **`get_word(difficulty, category)`** - Təsadüfi söz qaytarır
2. **`get_categories(difficulty)`** - Verilən çətinlik üçün kateqoriyaları qaytarır
3. **`get_difficulties()`** - Bütün çətinlik səviyyələrini qaytarır

---

## Addım 3: Oyun Məntiqi (game_logic.py)

### Nə üçün lazımdır?

Oyunun bütün məntiqini ehtiva edir: hərf təxmin etmə, qalibiyyət yoxlama, vizual göstərici.

### Cursor AI-dan kömək almaq

> "Mənə game_logic.py faylı yarat. HangmanGame sinfi lazımdır. word (söz), guessed_letters (təxmin edilmiş hərflər), wrong_guesses (səhv sayı) atributları lazımdır. guess_letter, get_display_word, check_winner, get_hangman_display funksiyaları lazımdır."

### HangmanGame Sinfi

**Atributlar:**
- `word` - Təxmin ediləcək söz (UPPERCASE)
- `guessed_letters` - Təxmin edilmiş hərflər (set)
- `wrong_guesses` - Səhv hərf sayı
- `max_wrong` - Maksimum səhv (6)
- `game_over` - Oyun bitib bitmədiyi
- `won` - Qalib gəlib gəlmədiyi

**Funksiyalar:**

1. **`__init__(self, word)`** - Oyunu başladır
2. **`guess_letter(self, letter)`** - Hərf təxmin edir
   - Hərf artıq təxmin edilibsə: "already_guessed"
   - Düzgün hərf: "correct"
   - Səhv hərf: "wrong", wrong_guesses += 1
   - Oyun bitdi: "won" və ya "lost"
3. **`get_display_word(self)`** - Sözü gizli formada göstərir
   - Təxmin edilmiş hərflər: hərf
   - Təxmin edilməmiş: "_"
4. **`is_word_complete(self)`** - Söz tam tapılıbmı yoxlayır
5. **`get_hangman_display(self)`** - Vizual göstərici (ASCII art)
6. **`get_status(self)`** - Oyun vəziyyətini qaytarır

### Vizual Göstərici

7 mərhələli ASCII art:
1. Boş (0 səhv)
2. Baş (1 səhv)
3. Bədən (2 səhv)
4. Bir əl (3 səhv)
5. İki əl (4 səhv)
6. Bir ayaq (5 səhv)
7. İki ayaq (6 səhv - oyun bitdi)

### Söz Göstərmə Alqoritmi

```python
def get_display_word(self):
    display = []
    for char in self.word:
        if char in self.guessed_letters:
            display.append(char)
        else:
            display.append("_")
    return " ".join(display)
```

---

## Addım 4: Verilənlər Bazası (database.py)

### Nə üçün lazımdır?

Oyun nəticələrini və statistikaları saxlayır.

### Cursor AI-dan kömək almaq

> "Mənə database.py faylı yarat. users, games (game_id, user_id, word, difficulty, category, won, wrong_guesses), statistics (user_id, games_played, games_won, games_lost, current_streak, best_streak) cədvəlləri lazımdır."

### Əsas Funksiyalar

1. **`save_game(user_id, word, difficulty, category, won, wrong_guesses)`** - Oyun nəticəsini saxlayır
2. **`update_statistics(user_id, won, wrong_guesses)`** - Statistikaları yeniləyir
   - Qalib: current_streak += 1, best_streak yenilə
   - Məğlub: current_streak = 0

---

## Addım 5: Telegram Bot (bot.py)

### Nə üçün lazımdır?

Botun əsas faylı.

### Cursor AI-dan kömək almaq

> "Mənə bot.py faylı yarat. /start, /newgame, /stats əmrləri lazımdır. Inline keyboard ilə çətinlik səviyyəsi, kateqoriya və hərf seçimi lazımdır. Azərbaycan əlifbası düymələri lazımdır."

### Bot Strukturu

**1. Çətinlik Səviyyəsi Seçimi:**
```python
keyboard = [
    [InlineKeyboardButton("🟢 Asan", callback_data="difficulty_asan")],
    [InlineKeyboardButton("🟡 Orta", callback_data="difficulty_orta")],
    [InlineKeyboardButton("🔴 Çətin", callback_data="difficulty_çətin")]
]
```

**2. Hərf Düymələri:**
```python
AZERBAIJAN_ALPHABET = "ABCÇDEƏFGĞHXIİJKQLMNOÖPRSŞTUÜVYZ"

# Hər hərf üçün düymə
for letter in AZERBAIJAN_ALPHABET:
    if letter in guessed:
        # Artıq təxmin edilmiş
        button = InlineKeyboardButton(f"❌ {letter}", callback_data=f"letter_used_{letter}")
    else:
        # Təxmin edilə bilər
        button = InlineKeyboardButton(letter, callback_data=f"letter_{letter}")
```

**3. Handler-lər:**
- `start()` - Botu başladır
- `new_game()` - Yeni oyun başladır
- `stats()` - Statistikaları göstərir
- `button_callback()` - Düymə basılmaları

### Oyun Axını

1. İstifadəçi `/newgame` yazır
2. Çətinlik səviyyəsi seçir
3. Kateqoriya seçir
4. Söz seçilir, oyun başlayır
5. Hərf seçir
6. Nəticə göstərilir (düzgün/səhv)
7. Vizual göstərici yenilənir
8. Oyun bitənə qədər davam edir
9. Nəticə göstərilir və statistika yenilənir

### Mesaj Formatlaşdırması

```
🎮 Oyun Davam Edir

📚 Kateqoriya: Heyvanlar
🎯 Çətinlik: Asan

   --------
   |      |
   |      O
   |     /|
   |
   |
=========

Söz: _ _ _ _ _

Təxmin edilmiş hərflər: A, B, C

Qalan cəhd: 3

Hərf seçin:
```

---

## Addım 6: Test və Debugging

### Test Etmə

1. **Oyun məntiqini test edin:**
   - Hərf təxmin etmə
   - Qalibiyyət yoxlama
   - Vizual göstərici

2. **Söz bazasını test edin:**
   - Söz seçimi
   - Çətinlik səviyyələri

3. **Botu test edin:**
   - Bütün əmrləri sınayın
   - Oyun axınını yoxlayın

### Ümumi Problemlər

**Problem:** Hərf təxmin edilmir
- **Həll:** Hərfləri UPPERCASE-ə çevirin. `letter.upper()`

**Problem:** Vizual göstərici düzgün göstərilmir
- **Həll:** ASCII art mərhələlərini düzgün yazın

**Problem:** Azərbaycan hərfləri işləmir
- **Həll:** Azərbaycan əlifbasını düzgün təyin edin

---

## Cursor AI İstifadəsi

### Tövsiyə Olunan Promptlar

1. **Oyun məntiqi üçün:**
   > "Mənə HangmanGame sinfi yarat. guess_letter funksiyası hərf təxmin etməli, get_display_word sözü gizli formada göstərməlidir."

2. **Vizual göstərici üçün:**
   > "Mənə get_hangman_display funksiyası yaz. 7 mərhələli ASCII art lazımdır - 0-dan 6-ya qədər səhv sayına görə."

3. **Hərf düymələri üçün:**
   > "Mənə Azərbaycan əlifbası üçün inline keyboard düymələri yarat. Hər hərf üçün düymə, artıq təxmin edilmiş hərflər üçün ❌ işarəsi."

---

## Tövsiyə Olunan İş Sırası

1. ✅ `config.py` yaradın
2. ✅ `word_database.py` yaradın - sözləri əlavə edin
3. ✅ `game_logic.py` yaradın - oyun məntiqini test edin
4. ✅ `database.py` yaradın
5. ✅ `bot.py` yaradın - botu test edin
6. ✅ Tam test edin

---

## Əlavə Məsləhətlər

1. **Söz bazası:**
   - Hər çətinlik üçün kifayət qədər söz
   - Azərbaycan dilində sözlər

2. **User experience:**
   - Aydın vizual göstərici
   - Emoji istifadə edin
   - Motivasiya mesajları

3. **Azərbaycan əlifbası:**
   - Xüsusi hərfləri dəstəkləyin
   - Ç, Ə, Ğ, İ, Ö, Ş, Ü

Uğurlar! 🎮