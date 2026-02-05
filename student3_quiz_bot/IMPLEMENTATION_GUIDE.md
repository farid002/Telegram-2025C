# Viktorina Master Bot - İmplementasiya Təlimatı

Bu təlimat sizə müxtəlif mövzularda viktorinalar təklif edən Telegram botunu addım-addım hazırlamağa kömək edəcək.

## Giriş

Bu layihədə müxtəlif mövzularda viktorinalar təklif edən bot hazırlayacaqsınız. Bot ilə biliklərinizi yoxlaya, xal toplaya və liderboard-da yer tuta biləcəksiniz.

### Nə qurulacaq?

1. **Sual Bazası** - Müxtəlif kateqoriyalarda suallar
2. **Viktorina Mühərriki** - Oyun məntiqi və idarəetmə
3. **Xal Sistemi** - Düzgün cavablar üçün xal
4. **Liderboard** - Ən yaxşı oyunçular
5. **Statistika** - Şəxsi nəticələr

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

> "Mənə config.py faylı yarat. BOT_TOKEN, DATABASE_FILE və QUESTIONS_PER_QUIZ (hər viktorinada neçə sual) parametrləri lazımdır."

---

## Addım 2: Sual Bazası (questions.py)

### Nə üçün lazımdır?

Müxtəlif kateqoriyalarda sualları saxlayır.

### Cursor AI-dan kömək almaq

> "Mənə questions.py faylı yarat. QUESTIONS_DATABASE sözlük strukturu lazımdır. Hər kateqoriya üçün suallar list-i. Hər sual üçün: question (sual mətni), options (4 seçim), correct (düzgün cavab indeksi). get_questions(category, count) və get_categories() funksiyaları lazımdır."

### Sual Strukturu

```python
{
    "question": "2 + 2 neçədir?",
    "options": ["3", "4", "5", "6"],
    "correct": 1  # "4" düzgün cavabdır (indeks 1)
}
```

### Kateqoriyalar

- riyaziyyat
- tarix
- elm
- ədəbiyyat
- idman
- coğrafiya

### Funksiyalar

1. **`get_questions(category, count)`** - Təsadüfi suallar qaytarır
2. **`get_categories()`** - Bütün kateqoriyaları qaytarır

### Təsadüfi Sual Seçimi

```python
import random
questions = QUESTIONS_DATABASE[category]
return random.sample(questions, min(count, len(questions)))
```

---

## Addım 3: Verilənlər Bazası (database.py)

### Nə üçün lazımdır?

Oyun nəticələrini və statistikaları saxlayır.

### Cursor AI-dan kömək almaq

> "Mənə database.py faylı yarat. 3 cədvəl lazımdır: users, quiz_games (game_id, user_id, category, score, total_questions), statistics (user_id, total_games, total_score, best_score). save_game, update_statistics, get_statistics, get_leaderboard funksiyaları lazımdır."

### Verilənlər Bazası Strukturu

**1. quiz_games cədvəli:**
- `game_id`, `user_id`, `category`
- `score` - Xal (düzgün cavab sayı)
- `total_questions` - Cəmi sual sayı

**2. statistics cədvəli:**
- `total_games` - Oynanılan oyunlar
- `total_score` - Cəmi xal
- `best_score` - Ən yaxşı nəticə (10-dan)

### Liderboard Sorğusu

```sql
SELECT u.first_name, s.best_score, s.total_games
FROM statistics s
JOIN users u ON s.user_id = u.user_id
ORDER BY s.best_score DESC, s.total_games DESC
LIMIT 10
```

---

## Addım 4: Viktorina Mühərriki (quiz_engine.py)

### Nə üçün lazımdır?

Viktorina oyununun məntiqini idarə edir.

### Cursor AI-dan kömək almaq

> "Mənə quiz_engine.py faylı yarat. QuizEngine sinfi lazımdır. start_quiz(user_id, category), get_current_question(user_id), answer_question(user_id, answer_index), is_finished(user_id), get_results(user_id) funksiyaları lazımdır."

### QuizEngine Sinfi

**Atributlar:**
- `user_quizzes` - {user_id: quiz_data} - Aktiv oyunlar

**quiz_data strukturu:**
```python
{
    "category": "riyaziyyat",
    "questions": [...],  # Sual list-i
    "current_question": 0,  # Cari sual indeksi
    "score": 0,  # Cari xal
    "answers": []  # Cavablar tarixçəsi
}
```

**Funksiyalar:**

1. **`start_quiz(user_id, category)`** - Yeni viktorina başladır
2. **`get_current_question(user_id)`** - Cari sualı qaytarır
3. **`answer_question(user_id, answer_index)`** - Suala cavab verir
   - Düzgün cavab: score += 1
   - Cavab tarixçəsinə əlavə et
   - current_question += 1
4. **`is_finished(user_id)`** - Oyun bitib bitmədiyini yoxlayır
5. **`get_results(user_id)`** - Oyun nəticələrini qaytarır
6. **`end_quiz(user_id)`** - Oyunu bitirir

### Sual Formatlaşdırması

```python
def format_question(question_data, question_num, total):
    text = f"❓ Sual {question_num}/{total}\n\n"
    text += f"{question_data['question']}\n\n"
    options_emoji = ["A", "B", "C", "D"]
    for i, option in enumerate(question_data['options']):
        text += f"{options_emoji[i]}) {option}\n"
    return text
```

---

## Addım 5: Telegram Bot (bot.py)

### Nə üçün lazımdır?

Botun əsas faylı.

### Cursor AI-dan kömək almaq

> "Mənə bot.py faylı yarat. /start, /quiz, /stats, /leaderboard əmrləri lazımdır. Inline keyboard ilə kateqoriya seçimi və cavab seçimləri lazımdır. Callback query handler ilə cavabları idarə etməliyəm."

### Bot Strukturu

**1. Kateqoriya Seçimi:**
```python
keyboard = [
    [InlineKeyboardButton("🔢 Riyaziyyat", callback_data="category_riyaziyyat")],
    [InlineKeyboardButton("📜 Tarix", callback_data="category_tarix")],
    # ...
]
```

**2. Cavab Düymələri:**
```python
keyboard = []
options_emoji = ["A", "B", "C", "D"]
for i, option in enumerate(question['options']):
    keyboard.append([InlineKeyboardButton(
        f"{options_emoji[i]}) {option}",
        callback_data=f"answer_{i}"
    )])
```

**3. Handler-lər:**
- `start()` - Botu başladır
- `quiz()` - Viktorina başladır
- `stats()` - Statistikaları göstərir
- `leaderboard()` - Liderboard göstərir
- `button_callback()` - Düymə basılmaları

### Oyun Axını

1. İstifadəçi `/quiz` yazır
2. Kateqoriya seçir
3. İlk sual göstərilir
4. Cavab seçir
5. Nəticə göstərilir (düzgün/səhv)
6. Növbəti sual
7. 10 sual bitdikdən sonra nəticə göstərilir
8. Statistika yenilənir

### Xal Hesablaması

- Hər düzgün cavab = 1 xal
- Maksimum = 10/10
- Faiz = (score / total) * 100

---

## Addım 6: Test və Debugging

### Test Etmə

1. **Sual bazasını test edin:**
   - Sual seçimi
   - Təsadüfi seçim

2. **Viktorina mühərrikini test edin:**
   - Oyun başlatma
   - Cavab vermə
   - Nəticə hesablama

3. **Botu test edin:**
   - Bütün əmrləri sınayın
   - Oyun axınını yoxlayın

### Ümumi Problemlər

**Problem:** Sual təkrarlanır
- **Həll:** `random.sample()` istifadə edin, `random.choice()` deyil

**Problem:** Xal düzgün hesablanmır
- **Həll:** answer_index ilə correct indeksini müqayisə edin

---

## Cursor AI İstifadəsi

### Tövsiyə Olunan Promptlar

1. **Sual bazası üçün:**
   > "Mənə questions.py faylı yarat. Müxtəlif kateqoriyalarda suallar olan sözlük strukturu lazımdır. Hər sual üçün question, options (4 seçim), correct (düzgün cavab indeksi) olmalıdır."

2. **Viktorina mühərriki üçün:**
   > "Mənə QuizEngine sinfi yarat. start_quiz, answer_question, get_results funksiyaları lazımdır. Oyun vəziyyətini idarə etməliyəm."

3. **Liderboard üçün:**
   > "Mənə get_leaderboard funksiyası yaz. SQL sorğusu ilə ən yaxşı nəticələri qaytarmalıdır."

---

## Tövsiyə Olunan İş Sırası

1. ✅ `config.py` yaradın
2. ✅ `questions.py` yaradın - sualları əlavə edin
3. ✅ `database.py` yaradın
4. ✅ `quiz_engine.py` yaradın - oyun məntiqini test edin
5. ✅ `bot.py` yaradın - botu test edin
6. ✅ Tam test edin

---

## Əlavə Məsləhətlər

1. **Sual bazası:**
   - Ən azı 10-15 sual hər kateqoriyada
   - Müxtəlif çətinlik səviyyələri

2. **User experience:**
   - Emoji istifadə edin
   - Aydın sual formatı
   - Düzgün/səhv cavab feedback-i

3. **Performans:**
   - Sual seçimi sürətli olmalıdır
   - Verilənlər bazası sorğuları optimallaşdırın

Uğurlar! 🎯