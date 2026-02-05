"""
Hesabatlar - statistika və hesabatların yaradılması
"""
import logging
from datetime import date, timedelta
from database import Database
from config import EXPENSE_CATEGORIES

logger = logging.getLogger(__name__)


class Reports:
    def __init__(self, db: Database):
        """Hesabat obyektini yaradır"""
        self.db = db

    def get_daily_report(self, user_id):
        """Günlük hesabat yaradır"""
        today = date.today()
        expenses = self.db.get_expenses(user_id, start_date=today, end_date=today)
        income = self.db.get_income(user_id, start_date=today, end_date=today)
        
        total_expenses = sum(exp[1] for exp in expenses)
        total_income = sum(inc[1] for inc in income)
        balance = total_income - total_expenses
        
        text = f"📊 Günlük Hesabat ({today})\n\n"
        text += f"💰 Gəlir: {total_income:.2f} AZN\n"
        text += f"💸 Xərc: {total_expenses:.2f} AZN\n"
        text += f"📈 Balans: {balance:.2f} AZN\n\n"
        
        if expenses:
            text += "📋 Xərclər:\n"
            for _, amount, category, description, _ in expenses[:5]:
                emoji = EXPENSE_CATEGORIES.get(category, "📝")
                text += f"  {emoji} {amount:.2f} AZN - {category}\n"
            if len(expenses) > 5:
                text += f"  ... və {len(expenses) - 5} digər\n"
        
        return text

    def get_monthly_report(self, user_id, year=None, month=None):
        """Aylıq hesabat yaradır"""
        if year is None or month is None:
            today = date.today()
            year = today.year
            month = today.month
        
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1)
        else:
            end_date = date(year, month + 1, 1)
        
        expenses = self.db.get_expenses(user_id, start_date=start_date, end_date=end_date)
        income = self.db.get_income(user_id, start_date=start_date, end_date=end_date)
        
        total_expenses = sum(exp[1] for exp in expenses)
        total_income = sum(inc[1] for inc in income)
        balance = total_income - total_expenses
        
        month_names = ["Yanvar", "Fevral", "Mart", "Aprel", "May", "İyun",
                      "İyul", "Avqust", "Sentyabr", "Oktyabr", "Noyabr", "Dekabr"]
        
        text = f"📊 Aylıq Hesabat ({month_names[month-1]} {year})\n\n"
        text += f"💰 Gəlir: {total_income:.2f} AZN\n"
        text += f"💸 Xərc: {total_expenses:.2f} AZN\n"
        text += f"📈 Balans: {balance:.2f} AZN\n\n"
        
        # Kateqoriyalar üzrə
        category_totals = {}
        for _, amount, category, _, _ in expenses:
            if category not in category_totals:
                category_totals[category] = 0.0
            category_totals[category] += amount
        
        if category_totals:
            text += "📋 Kateqoriyalar üzrə:\n"
            sorted_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
            for category, total in sorted_categories:
                emoji = EXPENSE_CATEGORIES.get(category, "📝")
                percentage = (total / total_expenses * 100) if total_expenses > 0 else 0
                text += f"  {emoji} {category}: {total:.2f} AZN ({percentage:.1f}%)\n"
        
        return text

    def get_budget_status(self, user_id):
        """Büdcə vəziyyətini göstərir"""
        budgets = self.db.get_budgets(user_id)
        if not budgets:
            return "📊 Büdcə təyin edilməyib."
        
        today = date.today()
        start_date = date(today.year, today.month, 1)
        if today.month == 12:
            end_date = date(today.year + 1, 1, 1)
        else:
            end_date = date(today.year, today.month + 1, 1)
        
        text = "📊 Büdcə Vəziyyəti:\n\n"
        
        for category, budget_amount, period in budgets:
            expenses = self.db.get_expenses(user_id, start_date=start_date, end_date=end_date, category=category)
            spent = sum(exp[1] for exp in expenses)
            remaining = budget_amount - spent
            percentage = (spent / budget_amount * 100) if budget_amount > 0 else 0
            
            emoji = EXPENSE_CATEGORIES.get(category, "📝")
            status_emoji = "✅" if remaining >= 0 else "⚠️"
            
            text += f"{emoji} {category.capitalize()}\n"
            text += f"  Büdcə: {budget_amount:.2f} AZN\n"
            text += f"  Xərc: {spent:.2f} AZN ({percentage:.1f}%)\n"
            text += f"  {status_emoji} Qalan: {remaining:.2f} AZN\n\n"
        
        return text