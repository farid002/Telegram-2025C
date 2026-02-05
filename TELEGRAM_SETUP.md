# Telegram Bot Qurulumu - Müəllim üçün Təlimat

Bu təlimat Telegram-da bot yaratmaq və konfiqurasiya etmək üçündür.

## Addım 1: BotFather ilə Bot Yaratmaq

### 1.1 BotFather-ə Müraciət

1. Telegram-da axtarışdan `@BotFather` tapın və ya bu linkə keçin: https://t.me/BotFather
2. BotFather-ə `/start` yazın
3. BotFather sizə əmrlər siyahısını göstərəcək

### 1.2 Yeni Bot Yaratmaq

1. BotFather-ə `/newbot` yazın
2. Bot üçün **ad** seçin (məsələn: "Mənim X-O Botum")
   - Bu ad Telegram-da görünəcək
3. Bot üçün **username** seçin (məsələn: `my_xo_bot`)
   - Bu username `_bot` ilə bitməlidir
   - Unikal olmalıdır (başqası tərəfindən istifadə edilməmiş olmalıdır)
   - Yalnız kiçik hərflər, rəqəmlər və `_` simvolu ola bilər

4. BotFather sizə **token** verəcək:
   ```
   123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   ```
   - Bu token-i **qeyd edin** - sonra lazım olacaq!
   - Token gizli saxlanılmalıdır

### 1.3 Bot Parametrlərini Təyin Etmək (İstəyə görə)

#### Bot Təsviri
```
/setdescription
```
Botunuzu seçin və təsvir yazın (məsələn: "X-O oyunu oynayın!")

#### Bot Haqqında
```
/setabouttext
```
Bot haqqında məlumat yazın

#### Bot Şəkli
```
/setuserpic
```
Bot üçün şəkil yükləyin (512x512 px tövsiyə olunur)

#### Bot Komandaları
```
/setcommands
```
Botunuzu seçin və əmrləri təyin edin:
```
start - Botu başlat
newgame - Yeni oyun başlat
stats - Statistikaları görün
help - Kömək
```

## Addım 2: Hər Tələbə üçün Bot Yaratmaq

Hər tələbə üçün ayrı bot yaratmalısınız:

1. **Student 1 üçün:**
   - `/newbot`
   - Ad: "X-O Oyun Botu"
   - Username: `student1_xo_bot` (və ya başqa unikal ad)
   - Token-i qeyd edin

2. **Student 2 üçün:**
   - `/newbot`
   - Ad: "Vərdiş İzləyici Bot"
   - Username: `student2_habit_bot`
   - Token-i qeyd edin

3. **Student 3 üçün:**
   - `/newbot`
   - Ad: "Viktorina Master Bot"
   - Username: `student3_quiz_bot`
   - Token-i qeyd edin

4. **Student 4 üçün:**
   - `/newbot`
   - Ad: "Adam Asma Oyunu Bot"
   - Username: `student4_hangman_bot`
   - Token-i qeyd edin

5. **Student 5 üçün:**
   - `/newbot`
   - Ad: "Xərclər İzləyici Bot"
   - Username: `student5_expense_bot`
   - Token-i qeyd edin

6. **Student 6 üçün:**
   - `/newbot`
   - Ad: "Söz Tapmacası Bot"
   - Username: `student6_word_puzzle_bot`
   - Token-i qeyd edin

## Addım 3: Token-ləri Təyin Etmək

Hər tələbə üçün:

1. `solution/studentX_*/` qovluğuna keçin
2. `.env.example` faylını `.env` adı ilə kopyalayın
3. `.env` faylına token əlavə edin:
   ```
   BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   ```

## Addım 4: Botları Test Etmək

Hər bot üçün:

1. Bot qovluğuna keçin: `cd solution/student1_xo_bot`
2. Virtual environment yaradın: `python3 -m venv venv`
3. Aktivləşdirin: `source venv/bin/activate`
4. Kitabxanaları quraşdırın: `pip install -r requirements.txt`
5. Botu işə salın: `python bot.py`
6. Telegram-da botu tapın və `/start` yazın

## Əlavə BotFather Əmrləri

### Bot Məlumatlarını Görmək
```
/mybots
```
Yaratdığınız botların siyahısını görürsünüz

### Bot Token-i Yeniləmək
```
/revoke
```
Köhnə token-i ləğv edir və yeni token verir

### Botu Silmək
```
/deletebot
```
Botu tamamilə silir (geri qaytarmaq mümkün deyil!)

## Təhlükəsizlik

⚠️ **Vacib:**
- Token-ləri **heç vaxt** public repository-lərə yükləməyin
- `.env` faylları `.gitignore`-da olmalıdır
- Token-ləri tələbələrlə paylaşarkən diqqətli olun
- Token oğurlanarsa, `/revoke` ilə yeniləyin

## Problem Həlləri

### Bot işə salınmır
- Token düzgün yazılıbmı? `.env` faylında yoxlayın
- İnternet əlaqəsi var?
- BotFather-dən token düzgün alınıbmı?

### Bot cavab vermir
- Bot işə salınıbmı? Terminalda xəta varmı?
- Token düzgündürmü?
- Bot Telegram-da aktivdirmi?

### Token xətası
- Token-də boşluq və ya xüsusi simvollar olmamalıdır
- Token-in sonunda `:` olmalıdır
- Token-i BotFather-dən yenidən alın

## Növbəti Addımlar

1. Bütün 6 bot üçün token alın
2. Hər bot üçün `.env` faylına token əlavə edin
3. Botları test edin
4. Tələbələrə token-ləri paylaşın (təhlükəsiz şəkildə)

## Kömək

- Telegram Bot API: https://core.telegram.org/bots/api
- BotFather: https://t.me/BotFather
- python-telegram-bot: https://python-telegram-bot.org/