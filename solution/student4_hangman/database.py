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
                word TEXT,
                difficulty TEXT,
                category TEXT,
                won INTEGER DEFAULT 0,
                wrong_guesses INTEGER,
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
                total_wrong_guesses INTEGER DEFAULT 0,
                best_streak INTEGER DEFAULT 0,
                current_streak INTEGER DEFAULT 0,
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

    def save_game(self, user_id, word, difficulty, category, won, wrong_guesses):
        """Oyun nəticəsini saxlayır"""
        try:
            self.cursor.execute("""
                INSERT INTO games (user_id, word, difficulty, category, won, wrong_guesses)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user_id, word, difficulty, category, 1 if won else 0, wrong_guesses))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Oyun saxlanarkən xəta: {e}")

    def update_statistics(self, user_id, won, wrong_guesses):
        """Statistikaları yeniləyir"""
        try:
            self.cursor.execute("""
                SELECT games_played, games_won, games_lost, total_wrong_guesses, current_streak, best_streak
                FROM statistics WHERE user_id = ?
            """, (user_id,))
            stats = self.cursor.fetchone()

            if stats:
                games_played, games_won, games_lost, total_wrong_guesses, current_streak, best_streak = stats
                
                games_played += 1
                if won:
                    games_won += 1
                    current_streak += 1
                    best_streak = max(best_streak, current_streak)
                else:
                    games_lost += 1
                    current_streak = 0
                
                total_wrong_guesses += wrong_guesses

                self.cursor.execute("""
                    UPDATE statistics
                    SET games_played = ?, games_won = ?, games_lost = ?, 
                        total_wrong_guesses = ?, current_streak = ?, best_streak = ?
                    WHERE user_id = ?
                """, (games_played, games_won, games_lost, total_wrong_guesses, current_streak, best_streak, user_id))
                self.conn.commit()
        except Exception as e:
            logger.error(f"Statistika yenilənərkən xəta: {e}")

    def get_statistics(self, user_id):
        """İstifadəçi statistikalarını qaytarır"""
        try:
            self.cursor.execute("""
                SELECT games_played, games_won, games_lost, total_wrong_guesses, current_streak, best_streak
                FROM statistics WHERE user_id = ?
            """, (user_id,))
            return self.cursor.fetchone()
        except Exception as e:
            logger.error(f"Statistika alınarkən xəta: {e}")
            return None

    def close(self):
        """Verilənlər bazası əlaqəsini bağlayır"""
        self.conn.close()