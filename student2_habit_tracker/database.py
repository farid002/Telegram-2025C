"""
Verilənlər bazası əməliyyatları - SQLite istifadəsi

TODO:
1. Database sinfi yaradın
2. users, habits, checkins cədvəllərini yaradın
3. add_user, add_habit, delete_habit, get_habits, checkin_habit, get_checkins, get_streak funksiyalarını yazın
"""

# TODO: Import-ları əlavə edin


class Database:
    def __init__(self):
        """Verilənlər bazasını yaradır"""
        # TODO: Verilənlər bazası əlaqəsi
        pass

    def init_database(self):
        """
        Cədvəlləri yaradır:
        - users (user_id, username, first_name)
        - habits (habit_id, user_id, habit_name, emoji)
        - checkins (checkin_id, habit_id, checkin_date - UNIQUE)
        """
        # TODO: CREATE TABLE sorğuları
        pass

    def add_user(self, user_id, username=None, first_name=None):
        """Yeni istifadəçi əlavə edir"""
        # TODO: İstifadəçi əlavə etmə
        pass

    def add_habit(self, user_id, habit_name, emoji="✅"):
        """Yeni vərdiş əlavə edir"""
        # TODO: Vərdiş əlavə etmə
        pass

    def delete_habit(self, habit_id, user_id):
        """Vərdişi silir"""
        # TODO: Vərdiş silmə
        pass

    def get_habits(self, user_id):
        """İstifadəçinin vərdişlərini qaytarır"""
        # TODO: Vərdişlər alma
        return []

    def checkin_habit(self, habit_id, checkin_date=None):
        """
        Vərdiş üçün gündəlik qeydiyyat edir
        
        TODO: INSERT OR IGNORE istifadə edin (UNIQUE constraint üçün)
        """
        # TODO: Qeydiyyat etmə
        pass

    def get_checkins(self, habit_id, start_date=None, end_date=None):
        """Vərdiş üçün qeydiyyatları qaytarır"""
        # TODO: Qeydiyyatlar alma
        return []

    def get_streak(self, habit_id):
        """
        Vərdiş üçün cari streak-i hesablayır
        
        TODO:
        1. Qeydiyyatları tarixə görə sırala
        2. Bu gündən geriyə doğru ardıcıl günləri say
        3. Kəsilmə olduqda dayan
        """
        # TODO: Streak hesablama
        return 0

    def close(self):
        """Verilənlər bazası əlaqəsini bağlayır"""
        pass