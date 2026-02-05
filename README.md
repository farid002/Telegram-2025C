# Telegram Bot Workshop 3

Bu repository 6 müxtəlif Telegram bot layihəsindən ibarətdir. Hər tələbə üçün tam müstəqil və funksional bot hazırlanmışdır.

## ⚠️ Qeyd

**Root səviyyəsində yalnız təlimatlar və sənədləşmə var.**
**Tam həllər `solution/` qovluğundadır və `.gitignore`-a əlavə edilmişdir.**

Tələbələr öz botlarını Cursor AI ilə hazırlamalıdırlar.

## Struktur

```
Telegram-2025C/
├── docs/                          # Sənədləşmə (tələbələr üçün)
│   ├── README.md                  # Ümumi workshop təlimatı
│   ├── telegram_bot_setup.md      # Telegram bot qurulumu
│   └── student1_xo_bot/          # Hər tələbə üçün sənədlər
│       ├── README.md
│       ├── setup_guide.md
│       └── technical_docs.md
│   └── ... (digər tələbələr)
├── student1_xo_bot/              # Tələbələr üçün - yalnız təlimatlar
│   ├── README.md                 # Layihə təsviri
│   ├── requirements.txt          # Lazımi kitabxanalar
│   └── .env.example              # Konfiqurasiya nümunəsi
├── student2_habit_tracker/
├── student3_quiz_bot/
├── student4_hangman/
├── student5_expense_tracker/
├── student6_word_puzzle/
├── solution/                      # Həllər (gitignore-da, müəllim üçün)
│   ├── docs/                     # Tam sənədləşmə
│   ├── student1_xo_bot/          # Tam həll (bütün kodlar)
│   └── ... (digər botlar)
├── README.md                      # Bu fayl
└── TELEGRAM_SETUP.md             # Telegram qurulum təlimatı
```

## Tələbələr üçün

1. Öz botunuzun qovluğuna keçin (məsələn: `student1_xo_bot/`)
2. `README.md` faylını oxuyun - layihə məqsədi və tələblər
3. `docs/student1_xo_bot/` qovluğundakı təlimatları oxuyun:
   - `setup_guide.md` - Bot qurulumu
   - `technical_docs.md` - Texniki detallar
4. Cursor AI ilə kod yazın
5. Botu quraşdırın və işə salın

## Müəllim üçün

**Həllər `solution/` qovluğundadır və `.gitignore`-a əlavə edilmişdir.**

`solution/` qovluğunda:
- Bütün botların tam həlləri (bütün kodlar)
- Tam sənədləşmə
- Hazır işləyən kodlar

Bu qovluq git-ə daxil edilmir və yalnız sizin üçündür.

## Layihələr

1. **Student 1: X-O Oyun Botu** (`student1_xo_bot/`)
   - Tic-Tac-Toe oyunu ilə AI rəqib
   - Minimax alqoritmi
   - Oyun statistikaları

2. **Student 2: Gündəlik Vərdiş İzləyici Bot** (`student2_habit_tracker/`)
   - Vərdiş izləmə və qeydiyyat
   - Streak izləməsi
   - Aylıq statistika

3. **Student 3: Viktorina Master Bot** (`student3_quiz_bot/`)
   - Müxtəlif mövzularda viktorinalar
   - Xal sistemi və liderboard
   - 6 kateqoriya

4. **Student 4: Adam Asma Oyunu Bot** (`student4_hangman/`)
   - Klassik hangman oyunu
   - Müxtəlif çətinlik səviyyələri
   - Vizual oyun göstəricisi

5. **Student 5: Xərclər İzləyici Bot** (`student5_expense_tracker/`)
   - Şəxsi maliyyə idarəetməsi
   - Xərc və gəlir qeydiyyatı
   - Hesabatlar və büdcə

6. **Student 6: Söz Tapmacası Bot** (`student6_word_puzzle/`)
   - Anagram həlledici
   - Söz yarışmaları
   - Gündəlik tapmacalar

## Quraşdırma

Hər bot üçün:

1. Bot qovluğuna keçin: `cd student1_xo_bot`
2. Virtual environment yaradın: `python3 -m venv venv`
3. Aktivləşdirin: `source venv/bin/activate`
4. Kitabxanaları quraşdırın: `pip install -r requirements.txt`
5. `.env.example` faylını `.env` adı ilə kopyalayın
6. `.env` faylına token əlavə edin
7. Cursor AI ilə kodları yazın
8. Botu işə salın: `python bot.py`

## Sənədləşmə

Ətraflı sənədləşmə `docs/` qovluğundadır:
- Ümumi təlimatlar
- Hər bot üçün addım-addım qurulum
- Texniki detallar

Bütün sənədlər **Azərbaycan dilində**dir.

## Texnologiyalar

- **Python 3.8+**
- **python-telegram-bot (v20+)**
- **SQLite3**
- **python-dotenv**

## Telegram Qurulumu

Telegram-da bot yaratmaq üçün `TELEGRAM_SETUP.md` faylına baxın.

## Lisenziya

Bu layihə təhsil məqsədi ilə hazırlanmışdır.