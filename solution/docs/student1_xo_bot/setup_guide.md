# X-O Bot Qurulum Təlimatı

## Addım 1: Telegram Bot Yaratmaq

1. Telegram-da `@BotFather` tapın
2. `/newbot` yazın və bot adı verin
3. Bot username seçin (məsələn: `my_xo_bot`)
4. BotFather-dən token alın və qeyd edin

## Addım 2: Proyekt Qovluğuna Keçin

```bash
cd student1_xo_bot
```

## Addım 3: Virtual Environment Yaradın

```bash
python3 -m venv venv
source venv/bin/activate  # Windows-da: venv\Scripts\activate
```

## Addım 4: Kitabxanaları Quraşdırın

```bash
pip install -r requirements.txt
```

Bu aşağıdakı kitabxanaları quraşdıracaq:
- `python-telegram-bot==20.7`
- `python-dotenv==1.0.0`

## Addım 5: Konfiqurasiya

1. `.env.example` faylını `.env` adı ilə kopyalayın:
   ```bash
   cp .env.example .env
   ```

2. `.env` faylını açın və token-i əlavə edin:
   ```
   BOT_TOKEN=your_bot_token_here
   ```
   `your_bot_token_here` yerinə BotFather-dən aldığınız token-i yazın.

## Addım 6: Botu İşə Salın

```bash
python bot.py
```

Əgər hər şey düzgündürsə, ekranda "Bot işə salınır..." mesajı görünəcək.

## Addım 7: Test Edin

1. Telegram-da botunuzu tapın
2. `/start` yazın
3. "Yeni Oyun Başlat" düyməsinə basın
4. Oyun taxtasındakı düymələrə basaraq hərəkət edin

## Problem Həlləri

### Bot işə salınmır
- `.env` faylında token düzgün yazılıbmı yoxlayın
- Terminalda xəta mesajı varmı?

### Düymələr işləmir
- Bot token-i düzgündürmü?
- İnternet əlaqəsi var?

### Verilənlər bazası xətası
- `xo_bot.db` faylı yaradıla bilirmi?
- Python-un yazma icazəsi varmı?

## Növbəti Addımlar

Bot işə salındıqdan sonra:
1. Kod strukturu ilə tanış olun
2. `technical_docs.md` faylını oxuyun
3. Öz dəyişikliklərinizi edin