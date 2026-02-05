# Xərclər İzləyici Bot - Texniki Sənədləşmə

## Kod Strukturu

### expense_manager.py

**ExpenseManager** sinfi:
- `add_expense()` - Xərc əlavə edir
- `get_category_totals()` - Kateqoriyalar üzrə ümumi
- `get_balance()` - Balans hesablayır

### reports.py

**Reports** sinfi:
- `get_daily_report()` - Günlük hesabat
- `get_monthly_report()` - Aylıq hesabat
- `get_budget_status()` - Büdcə vəziyyəti

## Verilənlər Bazası

```
expenses
├── expense_id
├── user_id
├── amount
├── category
├── description
└── expense_date

income
├── income_id
├── user_id
├── amount
└── income_date

budgets
├── budget_id
├── user_id
├── category
├── amount
└── period
```

## Kateqoriyalar

8 əsas kateqoriya:
- 🍔 Yemək
- 🚗 Nəqliyyat
- 🎬 Əyləncə
- 💊 Sağlamlıq
- 🛒 Alış-veriş
- 📚 Təhsil
- 🏠 Kommunal
- 📝 Digər