"""
Verilənlər bazası əməliyyatları - SQLite istifadəsi
"""
import sqlite3
import logging
from datetime import datetime
from config import DATABASE_FILE

logger = logging.getLogger(__name__)


class Database:
    def __init__(self):
        """Verilənlər bazasını yaradır və lazımi cədvəlləri hazırlayır"""
        self.conn = sqlite3.connect(DATABASE_FILE, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.init_database()

    def init_database(self):
        """Verilənlər bazası cədvəllərini yaradır"""
        # İstifadəçilər cədvəli
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Oyunlar cədvəli
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS games (
                game_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                result TEXT,
                moves_count INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)

        # Statistika cədvəli
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS statistics (
                user_id INTEGER PRIMARY KEY,
                games_played INTEGER DEFAULT 0,
                games_won INTEGER DEFAULT 0,
                games_lost INTEGER DEFAULT 0,
                games_draw INTEGER DEFAULT 0,
                win_streak INTEGER DEFAULT 0,
                best_streak INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)

        self.conn.commit()
        logger.info("Verilənlər bazası hazırlandı")

    def add_user(self, user_id, username=None, first_name=None):
        """Yeni istifadəçi əlavə edir"""
        try:
            self.cursor.execute("""
                INSERT OR IGNORE INTO users (user_id, username, first_name)
                VALUES (?, ?, ?)
            """, (user_id, username, first_name))
            self.cursor.execute("""
                INSERT OR IGNORE INTO statistics (user_id)
                VALUES (?)
            """, (user_id,))
            self.conn.commit()
        except Exception as e:
            logger.error(f"İstifadəçi əlavə edilərkən xəta: {e}")

    def save_game(self, user_id, result, moves_count):
        """Oyun nəticəsini saxlayır"""
        try:
            self.cursor.execute("""
                INSERT INTO games (user_id, result, moves_count)
                VALUES (?, ?, ?)
            """, (user_id, result, moves_count))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Oyun saxlanarkən xəta: {e}")

    def update_statistics(self, user_id, result):
        """Statistikaları yeniləyir"""
        try:
            # Cari statistikaları al
            self.cursor.execute("""
                SELECT games_played, games_won, games_lost, games_draw, win_streak, best_streak
                FROM statistics WHERE user_id = ?
            """, (user_id,))
            stats = self.cursor.fetchone()

            if stats:
                games_played, games_won, games_lost, games_draw, win_streak, best_streak = stats
                
                games_played += 1
                if result == "win":
                    games_won += 1
                    win_streak += 1
                    best_streak = max(best_streak, win_streak)
                elif result == "lose":
                    games_lost += 1
                    win_streak = 0
                elif result == "draw":
                    games_draw += 1
                    win_streak = 0

                self.cursor.execute("""
                    UPDATE statistics
                    SET games_played = ?, games_won = ?, games_lost = ?, 
                        games_draw = ?, win_streak = ?, best_streak = ?
                    WHERE user_id = ?
                """, (games_played, games_won, games_lost, games_draw, win_streak, best_streak, user_id))
                self.conn.commit()
        except Exception as e:
            logger.error(f"Statistika yenilənərkən xəta: {e}")

    def get_statistics(self, user_id):
        """İstifadəçi statistikalarını qaytarır"""
        try:
            self.cursor.execute("""
                SELECT games_played, games_won, games_lost, games_draw, win_streak, best_streak
                FROM statistics WHERE user_id = ?
            """, (user_id,))
            return self.cursor.fetchone()
        except Exception as e:
            logger.error(f"Statistika alınarkən xəta: {e}")
            return None

    def close(self):
        """Verilənlər bazası əlaqəsini bağlayır"""
        self.conn.close()