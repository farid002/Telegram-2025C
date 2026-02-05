# Adam Asma Bot - Texniki Sənədləşmə

## Kod Strukturu

### game_logic.py

**HangmanGame** sinfi:
- `guess_letter()` - Hərf təxmin edir
- `get_display_word()` - Gizli sözü göstərir
- `get_hangman_display()` - Vizual göstərici
- `check_winner()` - Qalibiyyəti yoxlayır

### word_database.py

Söz bazası çətinlik səviyyələrinə görə təşkil olunub:
- `WORDS_DATABASE` - Çətinlik → Kateqoriya → Sözlər
- `get_word()` - Təsadüfi söz qaytarır

## Vizual Göstərici

7 mərhələli ASCII art:
1. Boş
2. Baş
3. Bədən
4. Bir əl
5. İki əl
6. Bir ayaq
7. İki ayaq (oyun bitdi)

## Azərbaycan Əlifbası

Azərbaycan xüsusi hərfləri dəstəklənir:
`ABCÇDEƏFGĞHXIİJKQLMNOÖPRSŞTUÜVYZ`