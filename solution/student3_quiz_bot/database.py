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
            CREATE TABLE IF NOT EXISTS quiz_games (
                game_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                category TEXT,
                score INTEGER,
                total_questions INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)

        # Statistika cədvəli
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS statistics (
                user_id INTEGER PRIMARY KEY,
                total_games INTEGER DEFAULT 0,
                total_score INTEGER DEFAULT 0,
                total_questions INTEGER DEFAULT 0,
                best_score INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)

        # Liderboard üçün index
        self.cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_best_score ON statistics(best_score DESC)
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

    def save_game(self, user_id, category, score, total_questions):
        """Oyun nəticəsini saxlayır"""
        try:
            self.cursor.execute("""
                INSERT INTO quiz_games (user_id, category, score, total_questions)
                VALUES (?, ?, ?, ?)
            """, (user_id, category, score, total_questions))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Oyun saxlanarkən xəta: {e}")

    def update_statistics(self, user_id, score, total_questions):
        """Statistikaları yeniləyir"""
        try:
            self.cursor.execute("""
                SELECT total_games, total_score, total_questions, best_score
                FROM statistics WHERE user_id = ?
            """, (user_id,))
            stats = self.cursor.fetchone()

            if stats:
                total_games, total_score, total_questions_old, best_score = stats
                
                total_games += 1
                total_score += score
                total_questions_new = total_questions_old + total_questions
                best_score = max(best_score, score)

                self.cursor.execute("""
                    UPDATE statistics
                    SET total_games = ?, total_score = ?, total_questions = ?, best_score = ?
                    WHERE user_id = ?
                """, (total_games, total_score, total_questions_new, best_score, user_id))
                self.conn.commit()
        except Exception as e:
            logger.error(f"Statistika yenilənərkən xəta: {e}")

    def get_statistics(self, user_id):
        """İstifadəçi statistikalarını qaytarır"""
        try:
            self.cursor.execute("""
                SELECT total_games, total_score, total_questions, best_score
                FROM statistics WHERE user_id = ?
            """, (user_id,))
            return self.cursor.fetchone()
        except Exception as e:
            logger.error(f"Statistika alınarkən xəta: {e}")
            return None

    def get_leaderboard(self, limit=10):
        """Liderboard qaytarır"""
        try:
            self.cursor.execute("""
                SELECT u.first_name, u.username, s.best_score, s.total_games
                FROM statistics s
                JOIN users u ON s.user_id = u.user_id
                ORDER BY s.best_score DESC, s.total_games DESC
                LIMIT ?
            """, (limit,))
            return self.cursor.fetchall()
        except Exception as e:
            logger.error(f"Liderboard alınarkən xəta: {e}")
            return []

    def close(self):
        """Verilənlər bazası əlaqəsini bağlayır"""
        self.conn.close()