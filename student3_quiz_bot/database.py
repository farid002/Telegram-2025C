"""
Verilənlər bazası əməliyyatları

TODO:
1. users, quiz_games, statistics cədvəlləri
2. save_game, update_statistics, get_statistics, get_leaderboard funksiyaları
"""

# TODO: Import və Database sinfi


class Database:
    def __init__(self):
        """Verilənlər bazasını yaradır"""
        # TODO: Init kodunu yazın
        pass

    def init_database(self):
        """
        Cədvəlləri yaradır:
        - users
        - quiz_games (game_id, user_id, category, score, total_questions)
        - statistics (user_id, total_games, total_score, best_score)
        """
        # TODO: CREATE TABLE sorğuları
        pass

    def add_user(self, user_id, username=None, first_name=None):
        """Yeni istifadəçi əlavə edir"""
        # TODO: İstifadəçi əlavə etmə
        pass

    def save_game(self, user_id, category, score, total_questions):
        """Oyun nəticəsini saxlayır"""
        # TODO: Oyun saxlanma
        pass

    def update_statistics(self, user_id, score, total_questions):
        """
        Statistikaları yeniləyir
        
        TODO:
        1. Cari statistikaları al
        2. total_games, total_score artır
        3. best_score yenilə (əgər yeni nəticə daha yaxşıdırsa)
        """
        # TODO: Statistika yeniləmə
        pass

    def get_statistics(self, user_id):
        """İstifadəçi statistikalarını qaytarır"""
        # TODO: Statistika alma
        return None

    def get_leaderboard(self, limit=10):
        """
        Liderboard qaytarır
        
        TODO:
        1. statistics və users cədvəllərini JOIN et
        2. best_score-a görə sırala
        3. LIMIT ilə məhdudlaşdır
        4. List qaytar
        """
        # TODO: Liderboard sorğusu
        return []

    def close(self):
        """Verilənlər bazası əlaqəsini bağlayır"""
        pass