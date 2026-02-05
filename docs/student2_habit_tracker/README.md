# Student 2: Gündəlik Vərdiş İzləyici Bot

## Layihə Məqsədi

Bu layihədə gündəlik vərdişlərinizi izləyə biləcəyiniz Telegram bot hazırlayacaqsınız. Bot ilə vərdişlərinizi qeyd edə, streak-lərinizi izləyə və statistika görə biləcəksiniz.

## Nəticə

Layihəni tamamladıqdan sonra:
- Gündəlik vərdişlərinizi izləyə biləcəksiniz
- Streak (ardıcıl günlər) izləyə biləcəksiniz
- Aylıq statistika görə biləcəksiniz
- Təqvim görünüşü ilə vərdişlərinizi görə biləcəksiniz

## Əsas Xüsusiyyətlər

1. **Vərdiş Əlavə Etmə** - Yeni vərdişlər əlavə etmək
2. **Gündəlik Qeydiyyat** - Hər gün vərdişləri tamamlamaq
3. **Streak İzləməsi** - Ardıcıl günləri izləmək
4. **Statistika** - Aylıq və həftəlik hesabatlar
5. **Təqvim Görünüşü** - Vərdişlərin görsel təsviri

## Texniki Komponentlər

- **habit_manager.py** - Vərdiş idarəetməsi
- **statistics.py** - Statistika hesablamaları
- **database.py** - Verilənlər bazası
- **bot.py** - Telegram bot əsas faylı

## İstifadə Səhnələri

1. İstifadəçi vərdiş əlavə edir
2. Hər gün vərdişi tamamladıqda qeydiyyat edir
3. Streak-ləri izləyir
4. Aylıq statistika görür

## Öyrəniləcək Anlayışlar

- Tarix hesablamaları (datetime)
- Streak alqoritmi
- Təqvim görünüşü yaratma
- Reply keyboard buttons
- Verilənlər bazası münasibətləri