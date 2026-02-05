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

Layihə aşağıdakı fayllardan ibarət olmalıdır:

- **bot.py** - Telegram bot əsas faylı
- **game_logic.py** - Oyun məntiqi və Minimax alqoritmi
- **database.py** - Verilənlər bazası əməliyyatları
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

## 📖 İmplementasiya Təlimatı

**Ətraflı addım-addım təlimat üçün `IMPLEMENTATION_GUIDE.md` faylını oxuyun!**

Bu təlimatda:
- Hər fayl üçün ətraflı izahlar
- Cursor AI-dan necə kömək almaq
- Kod nümunələri və strukturlar
- Test və debugging məsləhətləri
- Problem həlləri

## Əlavə Sənədləşmə

`docs/student1_xo_bot/` qovluğunda:
- `setup_guide.md` - Bot qurulumu
- `technical_docs.md` - Texniki detallar

## Cursor AI ilə İşləmə

1. `IMPLEMENTATION_GUIDE.md` faylını oxuyun
2. Cursor AI-dan kömək alın (təlimatda tövsiyə olunan promptlar var)
3. Hər faylı addım-addım yazın
4. Test edin və düzəldin

## Tövsiyə Olunan İş Sırası

1. `IMPLEMENTATION_GUIDE.md` faylını oxuyun
2. `config.py` faylını yaradın
3. `database.py` faylını yaradın
4. `game_logic.py` faylını yaradın
5. `bot.py` faylını yaradın
6. Test edin
5. Test edin və düzəldin