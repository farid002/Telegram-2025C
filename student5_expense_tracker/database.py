"""
Verilənlər bazası əməliyyatları

TODO:
1. users, expenses, income, budgets cədvəlləri
2. add_expense, add_income, get_expenses, get_total_expenses, set_budget funksiyaları
"""

# TODO: Import və Database sinfi


class Database:
    def __init__(self):
        """Verilənlər bazasını yaradır"""
        # TODO: Init
        pass

    def init_database(self):
        """
        Cədvəlləri yaradır:
        - users
        - expenses (expense_id, user_id, amount REAL, category, description, expense_date)
        - income (income_id, user_id, amount REAL, description, income_date)
        - budgets (budget_id, user_id, category, amount REAL, period)
        """
        # TODO: CREATE TABLE
        pass

    def add_user(self, user_id, username=None, first_name=None):
        """Yeni istifadəçi əlavə edir"""
        # TODO: İstifadəçi əlavə etmə
        pass

    def add_expense(self, user_id, amount, category, description, expense_date=None):
        """Xərc əlavə edir"""
        # TODO: Xərc əlavə etmə
        pass

    def add_income(self, user_id, amount, description, income_date=None):
        """Gəlir əlavə edir"""
        # TODO: Gəlir əlavə etmə
        pass

    def get_expenses(self, user_id, start_date=None, end_date=None, category=None):
        """
        Xərcləri qaytarır
        
        TODO:
        1. WHERE şərtlərini dinamik yarat
        2. Tarix aralığı və kateqoriya filterləri
        3. ORDER BY expense_date DESC
        """
        # TODO: Xərclər alma
        return []

    def get_total_expenses(self, user_id, start_date=None, end_date=None):
        """Ümumi xərcləri hesablayır"""
        # TODO: SUM(amount) sorğusu
        return 0.0

    def get_total_income(self, user_id, start_date=None, end_date=None):
        """Ümumi gəlirləri hesablayır"""
        # TODO: SUM(amount) sorğusu
        return 0.0

    def set_budget(self, user_id, category, amount, period="monthly"):
        """
        Büdcə təyin edir
        
        TODO:
        1. Köhnə büdcəni sil
        2. Yeni büdcə əlavə et
        """
        # TODO: Büdcə təyin etmə
        pass

    def get_budgets(self, user_id):
        """Büdcələri qaytarır"""
        # TODO: Büdcələr alma
        return []

    def close(self):
        """Verilənlər bazası əlaqəsini bağlayır"""
        pass