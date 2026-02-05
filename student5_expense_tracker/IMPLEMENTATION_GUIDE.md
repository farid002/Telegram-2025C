# Xərclər İzləyici Bot - İmplementasiya Təlimatı

Bu təlimat sizə şəxsi maliyyənizi idarə edə biləcəyiniz Telegram botunu addım-addım hazırlamağa kömək edəcək.

## Giriş

Bu layihədə şəxsi maliyyənizi idarə edə biləcəyiniz bot hazırlayacaqsınız. Bot ilə xərclərinizi və gəlirlərinizi qeyd edə, hesabatlar görə biləcəksiniz.

### Nə qurulacaq?

1. **Xərc Qeydiyyatı** - Kateqoriyalarla xərc əlavə etmə
2. **Gəlir Qeydiyyatı** - Gəlir əlavə etmə
3. **Hesabatlar** - Günlük və aylıq hesabatlar
4. **Büdcə İzləməsi** - Büdcə vəziyyəti
5. **Balans Hesablaması** - Gəlir - Xərc

### Texnologiyalar

- Python 3.8+
- python-telegram-bot (v20+)
- SQLite3
- python-dotenv
- datetime modulu

---

## Addım 1: Konfiqurasiya (config.py)

### Nə üçün lazımdır?

Bot token-i və xərc kateqoriyalarını saxlayır.

### Cursor AI-dan kömək almaq

> "Mənə config.py faylı yarat. BOT_TOKEN, DATABASE_FILE və EXPENSE_CATEGORIES sözlük lazımdır. EXPENSE_CATEGORIES-də kateqoriya adı və emoji olmalıdır: {'yemək': '🍔', 'nəqliyyat': '🚗', ...}"

### Xərc Kateqoriyaları

```python
EXPENSE_CATEGORIES = {
    "yemək": "🍔",
    "nəqliyyat": "🚗",
    "əyləncə": "🎬",
    "sağlamlıq": "💊",
    "alış-veriş": "🛒",
    "təhsil": "📚",
    "kommunal": "🏠",
    "digər": "📝"
}
```

---

## Addım 2: Verilənlər Bazası (database.py)

### Nə üçün lazımdır?

Xərcləri, gəlirləri və büdcələri saxlayır.

### Cursor AI-dan kömək almaq

> "Mənə database.py faylı yarat. 4 cədvəl lazımdır: users, expenses (expense_id, user_id, amount, category, description, expense_date), income (income_id, user_id, amount, description, income_date), budgets (budget_id, user_id, category, amount, period). add_expense, add_income, get_expenses, get_total_expenses, set_budget funksiyaları lazımdır."

### Verilənlər Bazası Strukturu

**1. expenses cədvəli:**
- `expense_id`, `user_id`
- `amount` (REAL) - Məbləğ
- `category` - Kateqoriya
- `description` - Təsvir
- `expense_date` (DATE) - Tarix

**2. income cədvəli:**
- `income_id`, `user_id`
- `amount` (REAL)
- `description`
- `income_date` (DATE)

**3. budgets cədvəli:**
- `budget_id`, `user_id`
- `category` - Kateqoriya
- `amount` (REAL) - Büdcə məbləği
- `period` - Dövr (monthly, weekly)

### Əsas Funksiyalar

1. **`add_expense(user_id, amount, category, description, expense_date)`** - Xərc əlavə edir
2. **`add_income(user_id, amount, description, income_date)`** - Gəlir əlavə edir
3. **`get_expenses(user_id, start_date, end_date, category)`** - Xərcləri qaytarır
4. **`get_total_expenses(user_id, start_date, end_date)`** - Ümumi xərcləri hesablayır
5. **`get_total_income(user_id, start_date, end_date)`** - Ümumi gəlirləri hesablayır
6. **`set_budget(user_id, category, amount, period)`** - Büdcə təyin edir
7. **`get_budgets(user_id)`** - Büdcələri qaytarır

### Tarix Sorğuları

```sql
-- Aylıq xərclər
SELECT * FROM expenses 
WHERE user_id = ? 
AND expense_date >= '2024-02-01' 
AND expense_date < '2024-03-01'
```

---

## Addım 3: Xərc İdarəetməsi (expense_manager.py)

### Nə üçün lazımdır?

Xərclərlə işləmə məntiqini ehtiva edir.

### Cursor AI-dan kömək almaq

> "Mənə expense_manager.py faylı yarat. ExpenseManager sinfi lazımdır. add_expense, get_today_expenses, get_monthly_expenses, get_category_totals, get_balance funksiyaları lazımdır."

### ExpenseManager Sinfi

**Funksiyalar:**

1. **`add_expense(user_id, amount, category, description)`** - Xərc əlavə edir
2. **`add_income(user_id, amount, description)`** - Gəlir əlavə edir
3. **`get_today_expenses(user_id)`** - Bu günkü xərcləri qaytarır
4. **`get_monthly_expenses(user_id, year, month)`** - Aylıq xərcləri qaytarır
5. **`get_category_totals(user_id, start_date, end_date)`** - Kateqoriyalar üzrə ümumi xərcləri qaytarır
6. **`get_balance(user_id, start_date, end_date)`** - Balansı hesablayır (gəlir - xərc)
7. **`format_expense_list(expenses)`** - Xərc siyahısını formatlaşdırır

### Balans Hesablaması

```python
def get_balance(self, user_id, start_date=None, end_date=None):
    total_income = self.db.get_total_income(user_id, start_date, end_date)
    total_expenses = self.db.get_total_expenses(user_id, start_date, end_date)
    return total_income - total_expenses
```

---

## Addım 4: Hesabatlar (reports.py)

### Nə üçün lazımdır?

Hesabatların yaradılması və formatlaşdırılması.

### Cursor AI-dan kömək almaq

> "Mənə reports.py faylı yarat. Reports sinfi lazımdır. get_daily_report, get_monthly_report, get_budget_status funksiyaları lazımdır."

### Reports Sinfi

**Funksiyalar:**

1. **`get_daily_report(user_id)`** - Günlük hesabat
   - Bu günkü gəlir
   - Bu günkü xərc
   - Balans
   - Xərc siyahısı

2. **`get_monthly_report(user_id, year, month)`** - Aylıq hesabat
   - Aylıq gəlir
   - Aylıq xərc
   - Balans
   - Kateqoriyalar üzrə bölgü
   - Faizlə

3. **`get_budget_status(user_id)`** - Büdcə vəziyyəti
   - Hər kateqoriya üçün:
     - Büdcə məbləği
     - Xərc məbləği
     - Qalan məbləğ
     - Faiz

### Aylıq Hesabat Formatı

```
📊 Aylıq Hesabat (Fevral 2024)

💰 Gəlir: 2000.00 AZN
💸 Xərc: 1500.00 AZN
📈 Balans: 500.00 AZN

📋 Kateqoriyalar üzrə:
  🍔 yemək: 500.00 AZN (33.3%)
  🚗 nəqliyyat: 300.00 AZN (20.0%)
  ...
```

---

## Addım 5: Telegram Bot (bot.py)

### Nə üçün lazımdır?

Botun əsas faylı.

### Cursor AI-dan kömək almaq

> "Mənə bot.py faylı yarat. Reply keyboard buttons lazımdır: '➕ Xərc Əlavə Et', '💰 Gəlir Əlavə Et', '📊 Hesabatlar'. /start, /addexpense, /addincome, /report əmrləri lazımdır. Inline keyboard ilə kateqoriya seçimi lazımdır."

### Bot Strukturu

**1. Reply Keyboard:**
```python
keyboard = [
    [KeyboardButton("➕ Xərc Əlavə Et"), KeyboardButton("💰 Gəlir Əlavə Et")],
    [KeyboardButton("📊 Hesabatlar"), KeyboardButton("📋 Xərclərim")],
    [KeyboardButton("💵 Büdcə"), KeyboardButton("❓ Kömək")]
]
```

**2. İstifadəçi Vəziyyəti:**
```python
user_states = {}  # {user_id: {"action": "add_expense", "amount": 25.50}}
```

**3. Handler-lər:**
- `start()` - Botu başladır
- `add_expense()` - Xərc əlavə etmə
- `add_income()` - Gəlir əlavə etmə
- `show_report()` - Hesabat göstərir
- `show_expenses()` - Xərcləri göstərir
- `button_callback()` - Düymə basılmaları
- `handle_message()` - Mesajları idarə edir

### Xərc Əlavə Etmə Axını

1. İstifadəçi "➕ Xərc Əlavə Et" düyməsinə basır
2. Məbləğ yazılması tələb olunur
3. İstifadəçi məbləğ yazır (məsələn: 25.50)
4. Kateqoriya seçimi düymələri göstərilir
5. İstifadəçi kateqoriya seçir
6. Xərc əlavə edilir

### Hesabat Axını

1. İstifadəçi "📊 Hesabatlar" düyməsinə basır
2. Hesabat növü seçimi (Günlük/Aylıq/Büdcə)
3. Hesabat göstərilir

---

## Addım 6: Test və Debugging

### Test Etmə

1. **Verilənlər bazasını test edin:**
   - Xərc əlavə etmə
   - Gəlir əlavə etmə
   - Hesablamalar

2. **Tarix hesablamalarını test edin:**
   - Günlük hesabat
   - Aylıq hesabat
   - Büdcə izləməsi

3. **Botu test edin:**
   - Bütün əmrləri sınayın
   - Xərc/gəlir əlavə etməni yoxlayın
   - Hesabatları yoxlayın

### Ümumi Problemlər

**Problem:** Məbləğ düzgün saxlanmır
- **Həll:** REAL tipindən istifadə edin, TEXT deyil

**Problem:** Tarix sorğuları işləmir
- **Həll:** DATE formatını yoxlayın. `date.today()` istifadə edin

**Problem:** Büdcə hesablaması səhvdir
- **Həll:** Aylıq dövr üçün tarix aralığını düzgün hesablayın

---

## Cursor AI İstifadəsi

### Tövsiyə Olunan Promptlar

1. **Verilənlər bazası üçün:**
   > "Mənə database.py faylı yarat. expenses və income cədvəlləri lazımdır. REAL tipində amount sahəsi olmalıdır."

2. **Hesabat üçün:**
   > "Mənə get_monthly_report funksiyası yaz. Bu funksiya aylıq gəlir, xərc, balans və kateqoriyalar üzrə bölgü göstərməlidir."

3. **Büdcə üçün:**
   > "Mənə get_budget_status funksiyası yaz. Hər kateqoriya üçün büdcə, xərc, qalan və faiz göstərməlidir."

---

## Tövsiyə Olunan İş Sırası

1. ✅ `config.py` yaradın - kateqoriyaları təyin edin
2. ✅ `database.py` yaradın - cədvəlləri yoxlayın
3. ✅ `expense_manager.py` yaradın - xərc əməliyyatlarını test edin
4. ✅ `reports.py` yaradın - hesabatları test edin
5. ✅ `bot.py` yaradın - botu test edin
6. ✅ Tam test edin

---

## Əlavə Məsləhətlər

1. **Məbləğ formatı:**
   - REAL tipindən istifadə edin
   - Formatlaşdırma: `f"{amount:.2f} AZN"`

2. **Tarix idarəetməsi:**
   - `date.today()` - bu gün
   - `date(year, month, 1)` - ayın ilk günü
   - `timedelta(days=30)` - 30 gün əvvəl

3. **User experience:**
   - Emoji istifadə edin
   - Aydın formatlaşdırma
   - Faizləri göstərin

Uğurlar! 💰