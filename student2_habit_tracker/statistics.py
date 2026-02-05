"""
Statistika hesablamaları və formatlaşdırma

TODO:
1. Statistics sinfi yaradın
2. get_calendar_view - aylıq təqvim görünüşü
3. get_weekly_report - həftəlik hesabat
"""

# TODO: Import-ları əlavə edin
# from database import Database
# from datetime import date, timedelta


class Statistics:
    def __init__(self, db):
        """Statistika obyektini yaradır"""
        # TODO: self.db = db
        pass

    def get_calendar_view(self, habit_id, year, month):
        """
        Aylıq təqvim görünüşü yaradır
        
        TODO:
        1. Ayın ilk gününü tap
        2. İlk günün həftə gününü tap (0-6)
        3. Boş günlər üçün boşluq əlavə et
        4. Ayın bütün günlərini əlavə et
        5. Hər gün üçün qeydiyyat varmı yoxla (✅ və ya ⬜)
        6. Formatlaşdırılmış string qaytar
        """
        # TODO: Təqvim görünüşü yaratma
        return ""

    def get_weekly_report(self, user_id):
        """
        Həftəlik hesabat yaradır
        
        TODO:
        1. Son 7 gün üçün tarix aralığı
        2. Hər vərdiş üçün qeydiyyat sayı
        3. Streak məlumatları
        4. Formatlaşdırılmış string qaytar
        """
        # TODO: Həftəlik hesabat
        return ""