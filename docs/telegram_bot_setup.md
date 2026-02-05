# Telegram Bot Qurulumu - Ümumi Təlimat

Bu təlimat bütün botlar üçün Telegram bot yaratmaq və qurmaq üçün addım-addım təlimatdır.

## Addım 1: Telegram Bot Yaratmaq

1. **Telegram-da BotFather-ə mesaj göndərin:**
   - Telegram-da axtarışdan `@BotFather` tapın
   - BotFather-ə `/start` yazın

2. **Yeni bot yaradın:**
   - BotFather-ə `/newbot` yazın
   - Bot üçün ad seçin (məsələn: "Mənim X-O Botum")
   - Bot üçün username seçin (məsələn: "my_xo_bot") - bu `_bot` ilə bitməlidir

3. **Bot Token-i əldə edin:**
   - BotFather sizə token verəcək (məsələn: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)
   - Bu token-i qeyd edin - sonra lazım olacaq!

4. **Bot parametrlərini təyin edin (istəyə görə):**
   - `/setdescription` - Bot təsviri
   - `/setabouttext` - Bot haqqında məlumat
   - `/setuserpic` - Bot şəkli

## Addım 2: Python Mühiti Qurulumu

1. **Python yüklənib yoxlayın:**
   ```bash
   python3 --version
   ```
   Python 3.8 və ya daha yüksək olmalıdır.

2. **Virtual environment yaradın (tövsiyə olunur):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Windows-da: venv\Scripts\activate
   ```

3. **Kitabxanaları quraşdırın:**
   ```bash
   pip install -r requirements.txt
   ```

## Addım 3: Konfiqurasiya

1. **`.env` faylı yaradın:**
   - `.env.example` faylını `.env` adı ilə kopyalayın
   - Faylı açın və `BOT_TOKEN`-i BotFather-dən aldığınız token ilə əvəz edin

   ```
   BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   ```

## Addım 4: Botu İşə Salmaq

1. **Bot faylını işə salın:**
   ```bash
   python bot.py
   ```

2. **Bot işə salındığını yoxlayın:**
   - Telegram-da botunuzu tapın
   - `/start` yazın
   - Bot cavab verməlidir!

## Addım 5: Test Etmə

1. **Əsas funksiyaları test edin:**
   - Botun əsas əmrlərini sınayın
   - Düymələrin işlədiyini yoxlayın
   - Verilənlər bazasının yaradıldığını yoxlayın

## Problem Həlləri

### Bot işə salınmır
- `.env` faylında token düzgün yazılıbmı yoxlayın
- İnternet əlaqəsi var?
- `requirements.txt`-dəki bütün kitabxanalar quraşdırılıbmı?

### Token xətası
- Token-i BotFather-dən yenidən alın
- Token-də boşluq və ya xüsusi simvollar olmamalıdır

### Verilənlər bazası xətası
- Python-un yazma icazəsi varmı?
- `.db` faylı yaradıla bilirmi?

## Növbəti Addımlar

Bot işə salındıqdan sonra:
1. Botun bütün funksiyalarını sınayın
2. Kod strukturu ilə tanış olun
3. Öz dəyişikliklərinizi edin

## Kömək

Hər hansı problemlə qarşılaşsanız:
- Cursor AI-dan istifadə edin
- Müəllimə müraciət edin
- Telegram Bot API sənədləşməsinə baxın: https://core.telegram.org/bots/api