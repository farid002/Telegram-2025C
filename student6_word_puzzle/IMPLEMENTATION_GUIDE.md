# Söz Tapmacası Bot - İmplementasiya Təlimatı

Bu təlimat sizə müxtəlif söz oyunları təklif edən Telegram botunu addım-addım hazırlamağa kömək edəcək.

## Giriş

Bu layihədə müxtəlif söz oyunları təklif edən bot hazırlayacaqsınız. Bot ilə anagramlar həll edə, söz yarışmaları oynaya biləcəksiniz.

### Nə qurulacaq?

1. **Anagram Həlledici** - Hərflərdən sözlər tapmaq
2. **Anagram Tapmacası** - Qarışdırılmış hərfləri düzəltmək
3. **Söz Yarışması** - Qarışdırılmış sözü tapmaq
4. **Söz Uzunluğu Tapmacası** - Verilən hərflərdən söz tapmaq
5. **Gündəlik Tapmaca** - Hər gün yeni tapmaca

### Texnologiyalar

- Python 3.8+
- python-telegram-bot (v20+)
- SQLite3
- python-dotenv
- collections.Counter

---

## Addım 1: Konfiqurasiya (config.py)

### Nə üçün lazımdır?

Bot token-i və konfiqurasiya parametrlərini saxlayır.

### Cursor AI-dan kömək almaq

> "Mənə config.py faylı yarat. BOT_TOKEN və DATABASE_FILE parametrləri lazımdır."

---

## Addım 2: Söz Bazası (word_database.py)

### Nə üçün lazımdır?

Müxtəlif sözləri saxlayır.

### Cursor AI-dan kömək almaq

> "Mənə word_database.py faylı yarat. WORDS_DATABASE list lazımdır - müxtəlif sözlər. get_words_by_length(min_length, max_length), get_random_word(min_length, max_length), is_valid_word(word) funksiyaları lazımdır."

### Söz Bazası Strukturu

```python
WORDS_DATABASE = [
    # Asan sözlər
    "alma", "kitab", "ev", "gül", ...
    # Orta sözlər
    "kompyuter", "proqramlaşdırma", ...
    # Çətin sözlər
    "alqoritm", "kriptoqrafiya", ...
]
```

### Funksiyalar

1. **`get_words_by_length(min_length, max_length)`** - Uzunluğa görə sözləri qaytarır
2. **`get_random_word(min_length, max_length)`** - Təsadüfi söz qaytarır
3. **`is_valid_word(word)`** - Sözün etibarlı olub olmadığını yoxlayır

---

## Addım 3: Tapmaca Mühərriki (puzzle_engine.py)

### Nə üçün lazımdır?

Müxtəlif tapmaca növlərinin məntiqini ehtiva edir.

### Cursor AI-dan kömək almaq

> "Mənə puzzle_engine.py faylı yarat. AnagramSolver, WordScramble, WordLengthPuzzle, DailyPuzzle sinifləri lazımdır. AnagramSolver üçün get_anagrams funksiyası - verilən hərflərdən mümkün sözləri tapmalıdır."

### AnagramSolver Sinfi

**Funksiyalar:**

1. **`get_anagrams(letters)`** - Hərflərdən anagramlar tapır
   - Alqoritm:
     1. Verilən hərflərin sayını hesabla (Counter)
     2. Söz bazasındakı hər sözü yoxla
     3. Sözün hərfləri verilən hərflərdə varmı yoxla
     4. Uyğun sözləri qaytar

**Nümunə:**
```python
letters = "ALMA"
# Mümkün anagramlar: "ALMA", "LAMA", "MAL" (əgər bazada varsa)
```

### WordScramble Sinfi

**Funksiyalar:**

1. **`generate_scramble()`** - Söz yarışması yaradır
   - Söz seç
   - Hərfləri qarışdır
   - Qaytar: {"scrambled": "...", "answer": "...", "hint": "..."}

### WordLengthPuzzle Sinfi

**Funksiyalar:**

1. **`generate_puzzle()`** - Söz uzunluğu tapmacası yaradır
   - Uzunluq seç (4-10)
   - Həmin uzunluqda söz seç
   - Bəzi hərfləri aç (məsələn 2 hərf)
   - Qalanları "_" ilə gizlət

### DailyPuzzle Sinfi

**Funksiyalar:**

1. **`generate_daily_puzzle(seed)`** - Gündəlik tapmaca yaradır
   - Seed istifadə et (tarix əsasında)
   - Eyni gün üçün eyni tapmaca
   - Təsadüfi tapmaca növü seç (anagram/scramble/length)

### Anagram Alqoritmi İzahı

```python
from collections import Counter

def get_anagrams(letters):
    letters = letters.lower()
    letter_count = Counter(letters)  # Hər hərfin sayı
    
    anagrams = []
    for word in WORDS_DATABASE:
        word_count = Counter(word.lower())
        
        # Bütün hərflər mövcuddurmu?
        if all(word_count[char] <= letter_count.get(char, 0) 
               for char in word_count):
            anagrams.append(word)
    
    return sorted(anagrams, key=len, reverse=True)
```

---

## Addım 4: Verilənlər Bazası (database.py)

### Nə üçün lazımdır?

Tapmaca nəticələrini və statistikaları saxlayır.

### Cursor AI-dan kömək almaq

> "Mənə database.py faylı yarat. users, puzzles (puzzle_id, user_id, puzzle_type, solved, attempts), statistics (user_id, puzzles_solved, puzzles_attempted, anagrams_solved, scrambles_solved, length_puzzles_solved, current_streak, best_streak), daily_puzzles (user_id, puzzle_date, solved, attempts - PRIMARY KEY user_id, puzzle_date) cədvəlləri lazımdır."

### Əsas Funksiyalar

1. **`save_puzzle_attempt(user_id, puzzle_type, solved)`** - Tapmaca cəhdini saxlayır
2. **`update_statistics(user_id, puzzle_type, solved)`** - Statistikaları yeniləyir
3. **`get_daily_puzzle_status(user_id, puzzle_date)`** - Gündəlik tapmaca vəziyyətini qaytarır
4. **`mark_daily_puzzle_solved(user_id, puzzle_date)`** - Gündəlik tapmacanı həll edildi kimi qeyd edir

---

## Addım 5: Telegram Bot (bot.py)

### Nə üçün lazımdır?

Botun əsas faylı.

### Cursor AI-dan kömək almaq

> "Mənə bot.py faylı yarat. /start, /anagram <hərflər>, /puzzle, /daily, /stats əmrləri lazımdır. Inline keyboard ilə tapmaca növü seçimi lazımdır. handle_message ilə tapmaca cavablarını yoxlamaq lazımdır."

### Bot Strukturu

**1. Əsas Menyu:**
```python
keyboard = [
    [InlineKeyboardButton("🔤 Anagram Həlledici", callback_data="anagram_solver")],
    [InlineKeyboardButton("🎲 Anagram Tapmacası", callback_data="anagram_puzzle")],
    [InlineKeyboardButton("🔀 Söz Yarışması", callback_data="scramble")],
    [InlineKeyboardButton("📏 Söz Uzunluğu", callback_data="length_puzzle")],
    [InlineKeyboardButton("📅 Gündəlik Tapmaca", callback_data="daily_puzzle")],
    [InlineKeyboardButton("📊 Statistika", callback_data="statistics")]
]
```

**2. Handler-lər:**
- `start()` - Botu başladır
- `anagram_command()` - /anagram <hərflər> - Anagram həlledici
- `puzzle_command()` - /puzzle - Tapmaca başladır
- `daily_command()` - /daily - Gündəlik tapmaca
- `stats()` - Statistikaları göstərir
- `button_callback()` - Düymə basılmaları
- `handle_message()` - Tapmaca cavablarını yoxlayır

**3. İstifadəçi Vəziyyəti:**
```python
user_puzzles = {}  # {user_id: puzzle_data}
# puzzle_data: {"type": "anagram", "answer": "ALMA", ...}
```

### Anagram Həlledici Axını

1. İstifadəçi `/anagram ALMA` yazır
2. Bot hərflərdən mümkün sözləri tapır
3. Sözlər siyahısı göstərilir

### Tapmaca Axını

1. İstifadəçi tapmaca növü seçir
2. Tapmaca yaradılır
3. Tapmaca göstərilir
4. İstifadəçi cavab yazır
5. Cavab yoxlanılır
6. Düzgündürsə: statistika yenilənir
7. Səhvdirsə: yenidən cəhd etmə təklif olunur

### Gündəlik Tapmaca

- Seed istifadə edir (tarix əsasında)
- Eyni gün üçün eyni tapmaca
- Hər istifadəçi üçün ayrı-ayrı

---

## Addım 6: Test və Debugging

### Test Etmə

1. **Anagram alqoritmini test edin:**
   ```python
   anagrams = AnagramSolver.get_anagrams("ALMA")
   assert "ALMA" in anagrams
   ```

2. **Tapmaca mühərrikini test edin:**
   - Anagram tapmacası
   - Söz yarışması
   - Söz uzunluğu

3. **Botu test edin:**
   - Bütün əmrləri sınayın
   - Tapmacaları həll edin
   - Statistikaları yoxlayın

### Ümumi Problemlər

**Problem:** Anagram alqoritmi çox yavaş işləyir
- **Həll:** Söz bazasını kiçik saxlayın və ya optimallaşdırın

**Problem:** Gündəlik tapmaca hər dəfə fərqlidir
- **Həll:** Seed istifadə edin: `random.seed(date.today().toordinal())`

**Problem:** Cavab yoxlanmır
- **Həll:** `handle_message` funksiyasında `user_puzzles` yoxlayın

---

## Cursor AI İstifadəsi

### Tövsiyə Olunan Promptlar

1. **Anagram alqoritmi üçün:**
   > "Mənə get_anagrams funksiyası yaz. collections.Counter istifadə edərək verilən hərflərdən mümkün sözləri tapmalıyam."

2. **Tapmaca yaratmaq üçün:**
   > "Mənə WordScramble sinfi yarat. generate_scramble funksiyası söz seçib hərfləri qarışdırmalıdır."

3. **Gündəlik tapmaca üçün:**
   > "Mənə DailyPuzzle sinfi yarat. generate_daily_puzzle funksiyası seed istifadə edərək eyni gün üçün eyni tapmaca yaratmalıdır."

---

## Tövsiyə Olunan İş Sırası

1. ✅ `config.py` yaradın
2. ✅ `word_database.py` yaradın - sözləri əlavə edin
3. ✅ `puzzle_engine.py` yaradın - tapmaca məntiqini test edin
4. ✅ `database.py` yaradın
5. ✅ `bot.py` yaradın - botu test edin
6. ✅ Tam test edin

---

## Əlavə Məsləhətlər

1. **Söz bazası:**
   - Kifayət qədər söz
   - Müxtəlif uzunluqlarda
   - Azərbaycan dilində

2. **Anagram alqoritmi:**
   - Counter istifadə edin
   - Sürətli işləməlidir
   - Uzunluğa görə sıralayın

3. **User experience:**
   - Aydın tapmaca formatı
   - İpucu verin
   - Motivasiya mesajları

Uğurlar! 🧩