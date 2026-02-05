# Viktorina Bot - Texniki Sənədləşmə

## Kod Strukturu

### questions.py

Sual bazası müxtəlif kateqoriyalarda sualları ehtiva edir:
- `QUESTIONS_DATABASE` - Sözlük strukturu
- `get_questions()` - Təsadüfi suallar qaytarır
- `get_categories()` - Kateqoriyaları qaytarır

### quiz_engine.py

**QuizEngine** sinfi:
- `start_quiz()` - Yeni viktorina başladır
- `answer_question()` - Suala cavab verir
- `get_results()` - Nəticələri qaytarır

## Verilənlər Bazası

```
users
├── user_id
└── first_name

quiz_games
├── game_id
├── user_id
├── category
├── score
└── total_questions

statistics
├── user_id
├── total_games
├── total_score
├── best_score
└── total_questions
```

## Xal Sistemi

- Hər düzgün cavab = 1 xal
- Maksimum xal = 10/10
- Faiz hesablanması: (score / total) * 100

## Liderboard

SQL sorğusu ilə ən yaxşı nəticələr:
```sql
SELECT ... ORDER BY best_score DESC LIMIT 10
```