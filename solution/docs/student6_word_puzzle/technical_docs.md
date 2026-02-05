# Söz Tapmacası Bot - Texniki Sənədləşmə

## Kod Strukturu

### puzzle_engine.py

**AnagramSolver** sinfi:
- `get_anagrams()` - Hərflərdən anagramlar tapır
- `generate_anagram_puzzle()` - Anagram tapmacası yaradır

**WordScramble** sinfi:
- `generate_scramble()` - Söz yarışması yaradır

**WordLengthPuzzle** sinfi:
- `generate_puzzle()` - Söz uzunluğu tapmacası yaradır

**DailyPuzzle** sinfi:
- `generate_daily_puzzle()` - Seed ilə eyni gün üçün eyni tapmaca

## Anagram Alqoritmi

1. Verilən hərflərin sayını hesablayır (Counter)
2. Söz bazasındakı hər sözü yoxlayır
3. Sözün hərfləri verilən hərflərdə varmı yoxlayır
4. Uyğun sözləri qaytarır

## Gündəlik Tapmaca

Seed istifadəsi ilə eyni gün üçün eyni tapmaca:
```python
seed = date.today().toordinal()
random.seed(seed)
```

## Verilənlər Bazası

```
puzzles
├── puzzle_id
├── user_id
├── puzzle_type
├── solved
└── attempts

daily_puzzles
├── user_id
├── puzzle_date (PRIMARY KEY)
├── solved
└── attempts
```