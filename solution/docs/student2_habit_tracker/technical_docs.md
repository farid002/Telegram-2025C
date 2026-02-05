# Vərdiş İzləyici Bot - Texniki Sənədləşmə

## Kod Strukturu

### habit_manager.py

**HabitManager** sinfi vərdişlərlə işləmə məntiqini ehtiva edir:
- `add_habit()` - Yeni vərdiş
- `checkin_habit()` - Gündəlik qeydiyyat
- `get_habit_stats()` - Vərdiş statistikaları
- `format_habits_list()` - Vərdişlər siyahısını formatlaşdırır

### statistics.py

**Statistics** sinfi statistika hesablamalarını ehtiva edir:
- `get_calendar_view()` - Aylıq təqvim görünüşü
- `get_weekly_report()` - Həftəlik hesabat

### Streak Alqoritmi

Streak hesablama məntiqi:
1. Son qeydiyyat tarixini tapır
2. Bu gündən geriyə doğru ardıcıl günləri sayır
3. Kəsilmə olduqda streak-i sıfırlayır

## Verilənlər Bazası Sxemi

```
users
├── user_id
├── username
└── first_name

habits
├── habit_id
├── user_id
├── habit_name
└── emoji

checkins
├── checkin_id
├── habit_id
├── checkin_date (UNIQUE constraint)
└── created_at
```

## Tarix Hesablamaları

Python `datetime` modulundan istifadə:
- `date.today()` - Bu günün tarixi
- `timedelta(days=7)` - 7 gün əvvəl
- Tarix müqayisələri və hesablamalar

## Genişləndirmə İmkanları

1. Xatırlatmalar - Gecə saatında xatırlatma
2. Qrafiklər - Vizual statistika
3. Qruplar - Dostlarla vərdiş paylaşma
4. Mükafatlar - Streak mükafatları