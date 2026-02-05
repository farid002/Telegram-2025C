# Viktorina Bot Qurulum Təlimatı

## Addım 1: Telegram Bot Yaratmaq

1. `@BotFather` tapın
2. `/newbot` yazın
3. Bot adı və username verin
4. Token alın

## Addım 2: Proyekt Qovluğuna Keçin

```bash
cd student3_quiz_bot
```

## Addım 3: Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

## Addım 4: Kitabxanaları Quraşdırın

```bash
pip install -r requirements.txt
```

## Addım 5: Konfiqurasiya

1. `.env.example` → `.env` kopyalayın
2. Token əlavə edin

## Addım 6: Botu İşə Salın

```bash
python bot.py
```

## Addım 7: Test Edin

1. `/start` yazın
2. `/quiz` yazın
3. Kateqoriya seçin
4. Suallara cavab verin