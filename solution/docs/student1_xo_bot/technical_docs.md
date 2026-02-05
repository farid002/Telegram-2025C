# X-O Bot - Texniki Sənədləşmə

## Kod Strukturu

### bot.py - Əsas Bot Faylı

Bu fayl botun əsas məntiqini ehtiva edir:

- **start()** - Botu başladır, istifadəçini verilənlər bazasına əlavə edir
- **new_game()** - Yeni oyun başladır
- **button_callback()** - Düymə basılmalarını idarə edir
- **stats()** - Statistikaları göstərir

### game_logic.py - Oyun Məntiqi

**TicTacToe** sinfi:
- `board` - 3x3 oyun taxtası
- `make_move()` - Hərəkət edir
- `check_winner()` - Qalibiyyəti yoxlayır
- `get_best_move()` - AI üçün ən yaxşı hərəkəti tapır (Minimax)

**Minimax Alqoritmi:**
- Bütün mümkün oyun vəziyyətlərini yoxlayır
- İstifadəçi üçün ən pis, bot üçün ən yaxşı nəticəni seçir
- Rekursiv funksiya ilə həyata keçirilir

### database.py - Verilənlər Bazası

**Database** sinfi:
- `users` cədvəli - İstifadəçi məlumatları
- `games` cədvəli - Oyun tarixçəsi
- `statistics` cədvəli - İstifadəçi statistikaları

**Əsas funksiyalar:**
- `add_user()` - Yeni istifadəçi
- `save_game()` - Oyun nəticəsini saxlayır
- `update_statistics()` - Statistikaları yeniləyir
- `get_statistics()` - Statistikaları qaytarır

## Verilənlər Bazası Sxemi

```
users
├── user_id (PRIMARY KEY)
├── username
├── first_name
└── created_at

games
├── game_id (PRIMARY KEY)
├── user_id (FOREIGN KEY)
├── result (win/lose/draw)
├── moves_count
└── created_at

statistics
├── user_id (PRIMARY KEY)
├── games_played
├── games_won
├── games_lost
├── games_draw
├── win_streak
└── best_streak
```

## Telegram API İstifadəsi

### InlineKeyboardButton
Oyun taxtası düymələri üçün istifadə olunur:
```python
InlineKeyboardButton("1", callback_data="move_0_0")
```

### CallbackQueryHandler
Düymə basılmalarını idarə edir:
```python
application.add_handler(CallbackQueryHandler(button_callback))
```

## Alqoritmlər

### Minimax Alqoritmi

Minimax oyun nəzəriyyəsində istifadə olunan alqoritmdir:

1. Bütün mümkün hərəkətləri yoxlayır
2. Hər hərəkət üçün rekursiv olaraq nəticəni hesablayır
3. Bot üçün maksimum, istifadəçi üçün minimum dəyəri seçir
4. Ən yaxşı hərəkəti qaytarır

**Zaman mürəkkəbliyi:** O(b^d) burada b = branch factor, d = depth

## Genişləndirmə İmkanları

1. **Çox oyunçulu rejim** - İki istifadəçi bir-biri ilə oynaya bilər
2. **Çətinlik səviyyələri** - Asan, orta, çətin AI
3. **Turnir rejimi** - Bir neçə oyunçunun yarışması
4. **Görüntü ilə oyun taxtası** - Daha gözəl görünüş

## Test Etmə

1. Oyun məntiqini test edin:
   ```python
   game = TicTacToe()
   game.make_move(0, 0, 'X')
   assert game.check_winner() is None
   ```

2. Verilənlər bazasını test edin:
   ```python
   db = Database()
   db.add_user(123, "test_user")
   stats = db.get_statistics(123)
   assert stats is not None
   ```

## Performans

- **Oyun taxtası yoxlama:** O(1)
- **Minimax hesablama:** O(9^d) - praktikada çox sürətlidir
- **Verilənlər bazası sorğuları:** O(log n) - indexlər sayəsində

## Təhlükəsizlik

- İstifadəçi ID-ləri təhlükəsiz şəkildə saxlanılır
- SQL injection qorunması - parametrli sorğular
- Token `.env` faylında saxlanılır (git-ə daxil edilmir)