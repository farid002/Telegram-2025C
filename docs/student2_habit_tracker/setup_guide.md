# Vərdiş İzləyici Bot Qurulum Təlimatı

## Addım 1: Telegram Bot Yaratmaq

1. Telegram-da `@BotFather` tapın
2. `/newbot` yazın və bot adı verin (məsələn: "Mənim Vərdiş Botum")
3. Bot username seçin (məsələn: `my_habit_bot`)
4. BotFather-dən token alın

## Addım 2: Proyekt Qovluğuna Keçin

```bash
cd student2_habit_tracker
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

1. `.env.example` faylını `.env` adı ilə kopyalayın
2. `.env` faylına token əlavə edin:
   ```
   BOT_TOKEN=your_bot_token_here
   ```

## Addım 6: Botu İşə Salın

```bash
python bot.py
```

## Addım 7: Test Edin

1. Telegram-da botu tapın
2. `/start` yazın
3. "➕ Yeni Vərdiş" düyməsinə basın
4. Vərdiş adı yazın
5. Hər gün qeydiyyat edin

## Problem Həlləri

### Vərdiş əlavə edilmir
- Verilənlər bazası faylı yaradıla bilirmi?
- Python icazələri düzgündürmü?

### Streak hesablanmır
- Tarix formatı düzgündürmü?
- Verilənlər bazasında məlumat varmı?