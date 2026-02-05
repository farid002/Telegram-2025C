"""
Verilənlər bazası əməliyyatları

TODO:
1. users, games, statistics cədvəlləri
2. save_game, update_statistics, get_statistics funksiyaları
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
        - games (game_id, user_id, word, difficulty, category, won, wrong_guesses)
        - statistics (user_id, games_played, games_won, games_lost, current_streak, best_streak)
        """
        # TODO: CREATE TABLE
        pass

    def add_user(self, user_id, username=None, first_name=None):
        """Yeni istifadəçi əlavə edir"""
        # TODO: İstifadəçi əlavə etmə
        pass

    def save_game(self, user_id, word, difficulty, category, won, wrong_guesses):
        """Oyun nəticəsini saxlayır"""
        # TODO: Oyun saxlanma
        pass

    def update_statistics(self, user_id, won, wrong_guesses):
        """
        Statistikaları yeniləyir
        
        TODO:
        1. Qalibdirsə: current_streak += 1, best_streak yenilə
        2. Məğlubdur: current_streak = 0
        """
        # TODO: Statistika yeniləmə
        pass

    def get_statistics(self, user_id):
        """İstifadəçi statistikalarını qaytarır"""
        # TODO: Statistika alma
        return None

    def close(self):
        """Verilənlər bazası əlaqəsini bağlayır"""
        pass