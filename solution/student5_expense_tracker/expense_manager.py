"""
Xərc idarəetməsi - xərclərlə işləmə məntiqi
"""
import logging
from datetime import date, timedelta
from database import Database
from config import EXPENSE_CATEGORIES

logger = logging.getLogger(__name__)


class ExpenseManager:
    def __init__(self, db: Database):
        """Xərc idarəetməsi obyektini yaradır"""
        self.db = db

    def add_expense(self, user_id, amount, category, description):
        """Xərc əlavə edir"""
        return self.db.add_expense(user_id, amount, category, description)

    def add_income(self, user_id, amount, description):
        """Gəlir əlavə edir"""
        return self.db.add_income(user_id, amount, description)

    def get_today_expenses(self, user_id):
        """Bu günkü xərcləri qaytarır"""
        today = date.today()
        return self.db.get_expenses(user_id, start_date=today, end_date=today)

    def get_monthly_expenses(self, user_id, year, month):
        """Aylıq xərcləri qaytarır"""
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1)
        else:
            end_date = date(year, month + 1, 1)
        
        return self.db.get_expenses(user_id, start_date=start_date, end_date=end_date)

    def get_category_totals(self, user_id, start_date=None, end_date=None):
        """Kateqoriyalar üzrə ümumi xərcləri qaytarır"""
        expenses = self.db.get_expenses(user_id, start_date, end_date)
        totals = {}
        
        for _, amount, category, _, _ in expenses:
            if category not in totals:
                totals[category] = 0.0
            totals[category] += amount
        
        return totals

    def get_balance(self, user_id, start_date=None, end_date=None):
        """Balansı hesablayır (gəlir - xərc)"""
        total_income = self.db.get_total_income(user_id, start_date, end_date)
        total_expenses = self.db.get_total_expenses(user_id, start_date, end_date)
        return total_income - total_expenses

    def format_expense_list(self, expenses):
        """Xərc siyahısını formatlaşdırır"""
        if not expenses:
            return "📝 Xərc yoxdur."
        
        text = "📋 Xərclər:\n\n"
        total = 0.0
        
        for expense_id, amount, category, description, expense_date in expenses:
            emoji = EXPENSE_CATEGORIES.get(category, "📝")
            text += f"{emoji} {amount:.2f} AZN - {category}\n"
            if description:
                text += f"   📝 {description}\n"
            text += f"   📅 {expense_date}\n\n"
            total += amount
        
        text += f"💰 Ümumi: {total:.2f} AZN"
        return text