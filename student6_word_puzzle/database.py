"""
Verilənlər bazası əməliyyatları

TODO:
1. users, puzzles, statistics, daily_puzzles cədvəlləri
2. save_puzzle_attempt, update_statistics, get_daily_puzzle_status funksiyaları
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
        - puzzles (puzzle_id, user_id, puzzle_type, solved, attempts)
        - statistics (user_id, puzzles_solved, puzzles_attempted, anagrams_solved, scrambles_solved, length_puzzles_solved, current_streak, best_streak)
        - daily_puzzles (user_id, puzzle_date PRIMARY KEY, solved, attempts)
        """
        # TODO: CREATE TABLE
        pass

    def add_user(self, user_id, username=None, first_name=None):
        """Yeni istifadəçi əlavə edir"""
        # TODO: İstifadəçi əlavə etmə
        pass

    def save_puzzle_attempt(self, user_id, puzzle_type, solved):
        """Tapmaca cəhdini saxlayır"""
        # TODO: Puzzle cəhdi saxlanma
        pass

    def update_statistics(self, user_id, puzzle_type, solved):
        """
        Statistikaları yeniləyir
        
        TODO:
        1. Qalibdirsə: puzzles_solved += 1, current_streak += 1, best_streak yenilə
        2. puzzle_type-a görə uyğun counter artır
        3. Məğlubdur: current_streak = 0
        """
        # TODO: Statistika yeniləmə
        pass

    def get_statistics(self, user_id):
        """İstifadəçi statistikalarını qaytarır"""
        # TODO: Statistika alma
        return None

    def get_daily_puzzle_status(self, user_id, puzzle_date=None):
        """Gündəlik tapmaca vəziyyətini qaytarır"""
        # TODO: Gündəlik tapmaca vəziyyəti
        return None

    def mark_daily_puzzle_solved(self, user_id, puzzle_date=None):
        """Gündəlik tapmacanı həll edildi kimi qeyd edir"""
        # TODO: Gündəlik tapmaca qeyd etmə
        pass

    def close(self):
        """Verilənlər bazası əlaqəsini bağlayır"""
        pass