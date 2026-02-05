# Student 1: X-O Oyun Botu

## Layihə Məqsədi

Bu layihədə Telegram üzərində X-O (Tic-Tac-Toe) oyunu oynaya biləcəyiniz bot hazırlayacaqsınız. Bot AI rəqib ilə oynayacaq və oyun statistikalarınızı izləyəcək.

## Nəticə

Layihəni tamamladıqdan sonra:
- Telegram-da X-O oyunu oynaya biləcəksiniz
- AI rəqib ilə oyun oynayacaqsınız
- Oyun statistikalarınızı görə biləcəksiniz
- Minimax alqoritmi ilə tanış olacaqsınız

## Əsas Xüsusiyyətlər

1. **İnteraktiv Oyun Taxtası** - Düymələr ilə hərəkət etmək
2. **AI Rəqib** - Minimax alqoritmi ilə güclü rəqib
3. **Statistika** - Qalibiyyət/məğlubiyyət izləməsi
4. **Oyun Tarixçəsi** - Keçmiş oyunların qeydiyyatı

## Texniki Komponentlər

- **game_logic.py** - Oyun məntiqi və Minimax alqoritmi
- **database.py** - Verilənlər bazası əməliyyatları
- **bot.py** - Telegram bot əsas faylı
- **config.py** - Konfiqurasiya

## İstifadə Səhnələri

1. İstifadəçi botu başladır
2. Yeni oyun başladır
3. Düymələr ilə hərəkət edir
4. AI avtomatik cavab verir
5. Oyun bitir və statistika yenilənir

## Öyrəniləcək Anlayışlar

- Telegram Bot API
- Inline Keyboard Buttons
- Oyun məntiqi (game state management)
- Minimax alqoritmi
- SQLite verilənlər bazası
- Callback query handling