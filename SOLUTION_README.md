# Solution Folder - Müəllim üçün

Bu qovluq bütün botların **tam həllərini** ehtiva edir.

## Struktur

```
solution/
├── docs/                          # Tam sənədləşmə
│   ├── README.md
│   ├── telegram_bot_setup.md
│   └── student1_xo_bot/
│       ├── README.md
│       ├── setup_guide.md
│       └── technical_docs.md
│   └── ... (digər tələbələr)
├── student1_xo_bot/              # Tam həll
│   ├── bot.py                    # ✅ Tam kod
│   ├── game_logic.py
│   ├── database.py
│   ├── config.py
│   ├── requirements.txt
│   └── .env.example
├── student2_habit_tracker/       # Tam həll
├── student3_quiz_bot/            # Tam həll
├── student4_hangman/            # Tam həll
├── student5_expense_tracker/    # Tam həll
└── student6_word_puzzle/        # Tam həll
```

## İstifadə

Bu qovluq **yalnız sizin üçündür**:
- ✅ Git-ə daxil edilmir (`.gitignore`-da)
- ✅ Tələbələr görmür
- ✅ Tam işləyən kodlar
- ✅ Tam sənədləşmə

## Tələbələr üçün

Tələbələr **root səviyyəsindəki** qovluqlarla işləyirlər:
- `student1_xo_bot/` (root)
- `student2_habit_tracker/` (root)
- və s.

Onlar öz kodlarını yazmalıdırlar (Cursor AI ilə kömək ala bilərlər).

## Müqayisə

| | Root Level | Solution Folder |
|---|---|---|
| **Məqsəd** | Tələbələr üçün | Müəllim üçün |
| **Kod** | Tələbələr yazır | Tam həll |
| **Git** | Daxil edilir | İgnore edilir |
| **Görünür** | Hər kəs | Yalnız müəllim |

## Növbəti Addımlar

1. `solution/` qovluğundakı həlləri yoxlayın
2. Hər bot üçün token təyin edin
3. Botları test edin
4. Tələbələrə root səviyyəsindəki qovluqları verin