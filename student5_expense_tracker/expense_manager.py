"""
Xərc idarəetməsi - xərclərlə işləmə məntiqi

TODO:
1. ExpenseManager sinfi
2. add_expense, get_today_expenses, get_monthly_expenses, get_category_totals, get_balance funksiyaları
"""

# TODO: Import-ları əlavə edin
# from database import Database
# from datetime import date, timedelta
# from config import EXPENSE_CATEGORIES


class ExpenseManager:
    def __init__(self, db):
        """Xərc idarəetməsi obyektini yaradır"""
        # TODO: self.db = db
        pass

    def add_expense(self, user_id, amount, category, description):
        """Xərc əlavə edir"""
        # TODO: db.add_expense çağır
        pass

    def add_income(self, user_id, amount, description):
        """Gəlir əlavə edir"""
        # TODO: db.add_income çağır
        pass

    def get_today_expenses(self, user_id):
        """Bu günkü xərcləri qaytarır"""
        # TODO: date.today() ilə filter
        return []

    def get_monthly_expenses(self, user_id, year, month):
        """Aylıq xərcləri qaytarır"""
        # TODO: Ayın ilk və son günü ilə filter
        return []

    def get_category_totals(self, user_id, start_date=None, end_date=None):
        """
        Kateqoriyalar üzrə ümumi xərcləri qaytarır
        
        TODO:
        1. Xərcləri al
        2. Kateqoriyaya görə qruplaşdır
        3. SUM hesabla
        4. Dictionary qaytar {category: total}
        """
        # TODO: Kateqoriya ümumiləri
        return {}

    def get_balance(self, user_id, start_date=None, end_date=None):
        """
        Balansı hesablayır (gəlir - xərc)
        
        TODO:
        1. Ümumi gəlir al
        2. Ümumi xərc al
        3. Fərq qaytar
        """
        # TODO: Balans hesablama
        return 0.0

    def format_expense_list(self, expenses):
        """
        Xərc siyahısını formatlaşdırır
        
        TODO:
        1. Hər xərc üçün emoji, məbləğ, kateqoriya, təsvir, tarix göstər
        2. Ümumi məbləğ hesabla
        3. Formatlaşdırılmış string qaytar
        """
        # TODO: Formatlaşdırma
        return ""