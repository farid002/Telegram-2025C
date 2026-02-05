# Gündəlik Vərdiş İzləyici Bot - İmplementasiya Təlimatı

Bu təlimat sizə gündəlik vərdişlərinizi izləyə biləcəyiniz Telegram botunu addım-addım hazırlamağa kömək edəcək.

## Giriş

Bu layihədə gündəlik vərdişlərinizi izləyə biləcəyiniz bot hazırlayacaqsınız. Bot ilə vərdişlərinizi qeyd edə, streak-lərinizi izləyə və statistika görə biləcəksiniz.

### Nə qurulacaq?

1. **Vərdiş İdarəetməsi** - Vərdiş əlavə etmə, silmə, redaktə etmə
2. **Gündəlik Qeydiyyat** - Hər gün vərdişləri tamamlamaq
3. **Streak İzləməsi** - Ardıcıl günləri izləmək
4. **Statistika** - Aylıq və həftəlik hesabatlar
5. **Təqvim Görünüşü** - Vərdişlərin görsel təsviri

### Texnologiyalar

- Python 3.8+
- python-telegram-bot (v20+)
- SQLite3
- python-dotenv
- datetime modulu

---

## Addım 1: Konfiqurasiya (config.py)

### Nə üçün lazımdır?

Bot token-i və digər konfiqurasiya parametrlərini saxlayır.

### Cursor AI-dan kömək almaq

> "Mənə config.py faylı yarat. python-dotenv istifadə edərək .env faylından BOT_TOKEN oxumalıdır. Həmçinin DATABASE_FILE və REMINDER_HOUR (xatırlatma vaxtı) parametrləri olmalıdır."

### Nə yazılmalıdır?

- `BOT_TOKEN` - Telegram bot token
- `DATABASE_FILE` - Verilənlər bazası faylı
- `REMINDER_HOUR` - Xatırlatma vaxtı (məsələn: 20 = gecə 20:00)

---

## Addım 2: Verilənlər Bazası (database.py)

### Nə üçün lazımdır?

Vərdişləri, qeydiyyatları və istifadəçi məlumatlarını saxlayır.

### Cursor AI-dan kömək almaq

> "Mənə database.py faylı yarat. SQLite istifadə edərək 3 cədvəl lazımdır: users, habits (habit_id, user_id, habit_name, emoji), checkins (checkin_id, habit_id, checkin_date - UNIQUE). Database sinfi yarat və add_habit, delete_habit, get_habits, checkin_habit, get_checkins, get_streak funksiyaları əlavə et."

### Verilənlər Bazası Strukturu

**1. users cədvəli:**
- `user_id` (PRIMARY KEY)
- `username`, `first_name`
- `created_at`

**2. habits cədvəli:**
- `habit_id` (PRIMARY KEY, AUTOINCREMENT)
- `user_id` (FOREIGN KEY)
- `habit_name` - Vərdiş adı
- `emoji` - Vərdiş emoji-si
- `created_at`

**3. checkins cədvəli:**
- `checkin_id` (PRIMARY KEY, AUTOINCREMENT)
- `habit_id` (FOREIGN KEY)
- `checkin_date` (DATE, UNIQUE(habit_id, checkin_date)) - Hər vərdiş üçün hər gün yalnız bir qeydiyyat
- `created_at`

### Əsas Funksiyalar

1. **`add_habit(user_id, habit_name, emoji)`** - Yeni vərdiş əlavə edir
2. **`delete_habit(habit_id, user_id)`** - Vərdişi silir
3. **`get_habits(user_id)`** - İstifadəçinin vərdişlərini qaytarır
4. **`checkin_habit(habit_id, checkin_date)`** - Gündəlik qeydiyyat edir
5. **`get_checkins(habit_id, start_date, end_date)`** - Qeydiyyatları qaytarır
6. **`get_streak(habit_id)`** - Streak hesablayır

### Streak Hesablama Alqoritmi

Streak - ardıcıl günlərin sayıdır. Alqoritm:

1. Bu günün tarixini al
2. Son qeydiyyat tarixindən başla
3. Geriyə doğru ardıcıl günləri say
4. Kəsilmə olduqda (gün boşaldıqda) dayan

**Nümunə:**
- Bu gün: 5 Fevral
- Qeydiyyatlar: 5 Fev, 4 Fev, 3 Fev, 1 Fev
- Streak: 3 (5, 4, 3 - ardıcıl, 1-də kəsilib)

### SQL Nümunələri

```sql
-- checkins cədvəli - hər vərdiş üçün hər gün yalnız bir qeydiyyat
CREATE TABLE IF NOT EXISTS checkins (
    checkin_id INTEGER PRIMARY KEY AUTOINCREMENT,
    habit_id INTEGER,
    checkin_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (habit_id) REFERENCES habits(habit_id),
    UNIQUE(habit_id, checkin_date)
)
```

---

## Addım 3: Vərdiş İdarəetməsi (habit_manager.py)

### Nə üçün lazımdır?

Vərdişlərlə işləmə məntiqini ehtiva edir.

### Cursor AI-dan kömək almaq

> "Mənə habit_manager.py faylı yarat. HabitManager sinfi lazımdır. Database instance qəbul edir. add_habit, delete_habit, get_user_habits, checkin_habit, get_habit_stats, format_habits_list funksiyaları lazımdır."

### HabitManager Sinfi

**Funksiyalar:**

1. **`add_habit(user_id, habit_name, emoji)`** - Vərdiş əlavə edir
2. **`delete_habit(habit_id, user_id)`** - Vərdişi silir
3. **`get_user_habits(user_id)`** - İstifadəçinin vərdişlərini qaytarır
4. **`checkin_habit(habit_id, checkin_date)`** - Qeydiyyat edir
5. **`get_habit_stats(habit_id)`** - Vərdiş statistikalarını qaytarır:
   - Streak
   - Cəmi qeydiyyat sayı
   - Bu ay qeydiyyat sayı
   - Son 7 gün
   - Son 30 gün
6. **`format_habits_list(habits)`** - Vərdişlər siyahısını formatlaşdırır

### Tarix Hesablamaları

Python `datetime` modulundan istifadə:

```python
from datetime import date, timedelta

today = date.today()
week_ago = today - timedelta(days=7)
month_ago = today - timedelta(days=30)
```

---

## Addım 4: Statistika (statistics.py)

### Nə üçün lazımdır?

Statistika hesablamaları və formatlaşdırması.

### Cursor AI-dan kömək almaq

> "Mənə statistics.py faylı yarat. Statistics sinfi lazımdır. get_calendar_view funksiyası aylıq təqvim görünüşü yaratmalıdır - hər gün üçün ✅ (qeydiyyat var) və ya ⬜ (yoxdur) göstərməlidir. get_weekly_report funksiyası həftəlik hesabat yaratmalıdır."

### Statistics Sinfi

**Funksiyalar:**

1. **`get_calendar_view(habit_id, year, month)`** - Aylıq təqvim görünüşü
   - Həftə günləri başlığı
   - Hər gün üçün ✅ və ya ⬜
   - Formatlaşdırılmış görünüş

2. **`get_weekly_report(user_id)`** - Həftəlik hesabat
   - Son 7 gün üçün statistika
   - Hər vərdiş üçün qeydiyyat sayı
   - Streak məlumatları

### Təqvim Görünüşü Alqoritmi

1. Ayın ilk gününü tap
2. İlk günün həftə gününü tap (0-6)
3. Boş günlər üçün boşluq əlavə et
4. Ayın bütün günlərini əlavə et
5. Hər gün üçün qeydiyyat varmı yoxla
6. Formatlaşdır

---

## Addım 5: Telegram Bot (bot.py)

### Nə üçün lazımdır?

Botun əsas faylı - Telegram API ilə qarşılıqlı əlaqə.

### Cursor AI-dan kömək almaq

> "Mənə bot.py faylı yarat. python-telegram-bot v20 istifadə et. Reply keyboard buttons lazımdır: '📋 Vərdişlərim', '➕ Yeni Vərdiş', '📊 Statistika'. /start, /addhabit, /myhabits, /stats əmrləri lazımdır. Inline keyboard ilə vərdiş seçimi və emoji seçimi lazımdır."

### Bot Strukturu

**1. Reply Keyboard:**
```python
keyboard = [
    [KeyboardButton("📋 Vərdişlərim"), KeyboardButton("➕ Yeni Vərdiş")],
    [KeyboardButton("📊 Statistika"), KeyboardButton("📅 Təqvim")],
    [KeyboardButton("❓ Kömək")]
]
```

**2. Handler-lər:**
- `start()` - Botu başladır
- `add_habit()` - Yeni vərdiş əlavə etmə
- `my_habits()` - Vərdişləri göstərir
- `show_statistics()` - Statistikaları göstərir
- `button_callback()` - Düymə basılmaları
- `handle_message()` - Mesajları idarə edir

**3. İstifadəçi Vəziyyəti:**
```python
user_states = {}  # {user_id: {"action": "add_expense", "amount": 25.50}}
```

### Vərdiş Əlavə Etmə Axını

1. İstifadəçi "➕ Yeni Vərdiş" düyməsinə basır
2. Emoji seçimi düymələri göstərilir
3. İstifadəçi emoji seçir
4. Vərdiş adı yazılması tələb olunur
5. Vərdiş əlavə edilir

### Qeydiyyat Axını

1. İstifadəçi vərdiş seçir
2. "✅ Bu Gün Qeydiyyat Et" düyməsinə basır
3. Qeydiyyat edilir (əgər bu gün üçün yoxdursa)
4. Streak yenilənir
5. Statistikalar yenilənir

### Mesaj Formatlaşdırması

Emoji istifadə edin:
- ✅ - Qeydiyyat edilib
- 🔥 - Streak
- 📊 - Statistika
- 📅 - Tarix
- 💪 - Motivasiya

---

## Addım 6: Test və Debugging

### Test Etmə

1. **Verilənlər bazasını test edin:**
   - Vərdiş əlavə etmə
   - Qeydiyyat etmə
   - Streak hesablama

2. **Tarix hesablamalarını test edin:**
   - Streak alqoritmi
   - Aylıq statistika
   - Həftəlik hesabat

3. **Botu test edin:**
   - Bütün əmrləri sınayın
   - Düymələrin işlədiyini yoxlayın
   - Qeydiyyat sistemini yoxlayın

### Ümumi Problemlər

**Problem:** Streak düzgün hesablanmır
- **Həll:** Tarix formatını yoxlayın. `date.today()` istifadə edin, `datetime.now()` deyil.

**Problem:** Eyni gün üçün bir neçə qeydiyyat edilir
- **Həll:** UNIQUE constraint-i yoxlayın. `INSERT OR IGNORE` istifadə edin.

**Problem:** Təqvim görünüşü düzgün göstərilmir
- **Həll:** Həftə günü hesablamasını yoxlayın. Python-da `weekday()` 0-dan başlayır (Bazar ertəsi = 0).

---

## Cursor AI İstifadəsi

### Tövsiyə Olunan Promptlar

1. **Streak hesablama üçün:**
   > "Mənə get_streak funksiyası yaz. Bu funksiya vərdiş üçün ardıcıl günlərin sayını (streak) hesablamalıdır. Bu gündən geriyə doğru ardıcıl günləri saymalıdır."

2. **Təqvim görünüşü üçün:**
   > "Mənə get_calendar_view funksiyası yaz. Bu funksiya aylıq təqvim görünüşü yaratmalıdır. Həftə günləri başlığı, hər gün üçün ✅ və ya ⬜ göstərməlidir."

3. **Tarix əməliyyatları üçün:**
   > "Mənə Python datetime modulu ilə tarix hesablamaları üçün kod yaz. Bu gündən 7 gün əvvəl, 30 gün əvvəl tarixləri tapmalıyam."

---

## Tövsiyə Olunan İş Sırası

1. ✅ `config.py` yaradın
2. ✅ `database.py` yaradın - cədvəlləri yoxlayın
3. ✅ `habit_manager.py` yaradın - vərdiş əməliyyatlarını test edin
4. ✅ `statistics.py` yaradın - statistika funksiyalarını test edin
5. ✅ `bot.py` yaradın - botu test edin
6. ✅ Tam test edin

---

## Əlavə Məsləhətlər

1. **Tarix formatı:**
   - Həmişə `date` obyekti istifadə edin, string deyil
   - `date.today()` - bu gün
   - `date.fromisoformat("2024-02-05")` - string-dən date

2. **UNIQUE constraint:**
   - Hər vərdiş üçün hər gün yalnız bir qeydiyyat
   - `INSERT OR IGNORE` istifadə edin

3. **User experience:**
   - Emoji istifadə edin
   - Aydın mesajlar
   - Streak motivasiyası

Uğurlar! 💪