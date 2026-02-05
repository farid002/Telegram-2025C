"""
Verilənlər bazası əməliyyatları - SQLite istifadəsi

Bu faylı tamamlamaq üçün:
1. Database sinfi yaradın
2. init_database() funksiyası ilə cədvəlləri yaradın
3. add_user, save_game, update_statistics, get_statistics funksiyalarını yazın
"""

# TODO: Import-ları əlavə edin
# import sqlite3
# import logging
# from config import DATABASE_FILE

# logger = logging.getLogger(__name__)


class Database:
    def __init__(self):
        """
        Verilənlər bazasını yaradır və lazımi cədvəlləri hazırlayır
        
        TODO:
        1. SQLite əlaqəsi yaradın
        2. Cursor yaradın
        3. init_database() çağırın
        """
        # TODO: Verilənlər bazası əlaqəsini yaradın
        # self.conn = sqlite3.connect(...)
        # self.cursor = self.conn.cursor()
        # self.init_database()
        pass

    def init_database(self):
        """
        Verilənlər bazası cədvəllərini yaradır
        
        TODO: Aşağıdakı cədvəlləri yaradın:
        - users (user_id, username, first_name, created_at)
        - games (game_id, user_id, result, moves_count, created_at)
        - statistics (user_id, games_played, games_won, games_lost, games_draw, win_streak, best_streak)
        """
        # TODO: CREATE TABLE sorğularını yazın
        pass

    def add_user(self, user_id, username=None, first_name=None):
        """
        Yeni istifadəçi əlavə edir
        
        TODO:
        1. users cədvəlinə INSERT
        2. statistics cədvəlinə INSERT (default dəyərlərlə)
        3. commit edin
        """
        # TODO: İstifadəçi əlavə etmə kodunu yazın
        pass

    def save_game(self, user_id, result, moves_count):
        """
        Oyun nəticəsini saxlayır
        
        TODO:
        1. games cədvəlinə INSERT
        2. commit edin
        """
        # TODO: Oyun saxlanma kodunu yazın
        pass

    def update_statistics(self, user_id, result):
        """
        Statistikaları yeniləyir
        
        TODO:
        1. Cari statistikaları SELECT ilə alın
        2. result-a görə yeniləyin (win/lose/draw)
        3. win_streak və best_streak hesablayın
        4. UPDATE sorğusu ilə yeniləyin
        """
        # TODO: Statistika yeniləmə kodunu yazın
        pass

    def get_statistics(self, user_id):
        """
        İstifadəçi statistikalarını qaytarır
        
        TODO:
        1. statistics cədvəlindən SELECT
        2. Nəticəni qaytarın
        """
        # TODO: Statistika alma kodunu yazın
        return None

    def close(self):
        """Verilənlər bazası əlaqəsini bağlayır"""
        # TODO: self.conn.close()
        pass