"""
Vərdiş idarəetməsi - vərdişlərlə işləmə məntiqi

TODO:
1. HabitManager sinfi yaradın
2. Database instance qəbul edir
3. add_habit, delete_habit, get_user_habits, checkin_habit, get_habit_stats, format_habits_list funksiyalarını yazın
"""

# TODO: Import-ları əlavə edin
# from database import Database
# from datetime import date, timedelta


class HabitManager:
    def __init__(self, db):
        """Vərdiş idarəetməsi obyektini yaradır"""
        # TODO: self.db = db
        pass

    def add_habit(self, user_id, habit_name, emoji="✅"):
        """Yeni vərdiş əlavə edir"""
        # TODO: db.add_habit çağır
        pass

    def delete_habit(self, habit_id, user_id):
        """Vərdişi silir"""
        # TODO: db.delete_habit çağır
        pass

    def get_user_habits(self, user_id):
        """İstifadəçinin vərdişlərini qaytarır"""
        # TODO: db.get_habits çağır
        return []

    def checkin_habit(self, habit_id, checkin_date=None):
        """Vərdiş üçün qeydiyyat edir"""
        # TODO: db.checkin_habit çağır
        pass

    def get_habit_stats(self, habit_id):
        """
        Vərdiş statistikalarını qaytarır
        
        TODO:
        1. Streak hesabla
        2. Bu ay qeydiyyat sayı
        3. Son 7 gün qeydiyyat sayı
        4. Son 30 gün qeydiyyat sayı
        5. Cəmi qeydiyyat sayı
        6. Dictionary qaytar
        """
        # TODO: Statistika hesablama
        return {
            'streak': 0,
            'total': 0,
            'this_month': 0,
            'week': 0,
            'month': 0
        }

    def format_habits_list(self, habits):
        """
        Vərdişlər siyahısını formatlaşdırır
        
        TODO:
        1. Hər vərdiş üçün emoji, ad, streak, cəmi göstər
        2. Formatlaşdırılmış string qaytar
        """
        # TODO: Formatlaşdırma
        return ""