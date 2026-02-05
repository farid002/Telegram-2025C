"""
Hesabatlar - statistika və hesabatların yaradılması

TODO:
1. Reports sinfi
2. get_daily_report, get_monthly_report, get_budget_status funksiyaları
"""

# TODO: Import-ları əlavə edin
# from database import Database
# from datetime import date, timedelta
# from config import EXPENSE_CATEGORIES


class Reports:
    def __init__(self, db):
        """Hesabat obyektini yaradır"""
        # TODO: self.db = db
        pass

    def get_daily_report(self, user_id):
        """
        Günlük hesabat yaradır
        
        TODO:
        1. Bu günkü gəlir və xərc al
        2. Balans hesabla
        3. Xərc siyahısı (ilk 5)
        4. Formatlaşdırılmış string qaytar
        """
        # TODO: Günlük hesabat
        return ""

    def get_monthly_report(self, user_id, year=None, month=None):
        """
        Aylıq hesabat yaradır
        
        TODO:
        1. Aylıq gəlir və xərc al
        2. Balans hesabla
        3. Kateqoriyalar üzrə bölgü və faizlər
        4. Formatlaşdırılmış string qaytar
        """
        # TODO: Aylıq hesabat
        return ""

    def get_budget_status(self, user_id):
        """
        Büdcə vəziyyətini göstərir
        
        TODO:
        1. Büdcələri al
        2. Hər kateqoriya üçün:
           - Büdcə məbləği
           - Xərc məbləği (bu ay)
           - Qalan məbləğ
           - Faiz
        3. Formatlaşdırılmış string qaytar
        """
        # TODO: Büdcə vəziyyəti
        return ""