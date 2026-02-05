"""
Verilənlər bazası əməliyyatları - SQLite istifadəsi
"""
import sqlite3
import logging
from datetime import datetime, date
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
            CREATE TABLE IF NOT EXISTS puzzles (
                puzzle_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                puzzle_type TEXT,
                solved INTEGER DEFAULT 0,
                attempts INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)

        # Statistika cədvəli
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS statistics (
                user_id INTEGER PRIMARY KEY,
                puzzles_solved INTEGER DEFAULT 0,
                puzzles_attempted INTEGER DEFAULT 0,
                anagrams_solved INTEGER DEFAULT 0,
                scrambles_solved INTEGER DEFAULT 0,
                length_puzzles_solved INTEGER DEFAULT 0,
                current_streak INTEGER DEFAULT 0,
                best_streak INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)

        # Gündəlik tapmacalar cədvəli
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS daily_puzzles (
                user_id INTEGER,
                puzzle_date DATE,
                solved INTEGER DEFAULT 0,
                attempts INTEGER DEFAULT 0,
                PRIMARY KEY (user_id, puzzle_date),
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

    def save_puzzle_attempt(self, user_id, puzzle_type, solved):
        """Tapmaca cəhdini saxlayır"""
        try:
            self.cursor.execute("""
                INSERT INTO puzzles (user_id, puzzle_type, solved, attempts)
                VALUES (?, ?, ?, 1)
            """, (user_id, puzzle_type, 1 if solved else 0))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Tapmaca saxlanarkən xəta: {e}")

    def update_statistics(self, user_id, puzzle_type, solved):
        """Statistikaları yeniləyir"""
        try:
            self.cursor.execute("""
                SELECT puzzles_solved, puzzles_attempted, anagrams_solved, scrambles_solved, 
                       length_puzzles_solved, current_streak, best_streak
                FROM statistics WHERE user_id = ?
            """, (user_id,))
            stats = self.cursor.fetchone()

            if stats:
                puzzles_solved, puzzles_attempted, anagrams_solved, scrambles_solved, \
                length_puzzles_solved, current_streak, best_streak = stats
                
                puzzles_attempted += 1
                if solved:
                    puzzles_solved += 1
                    current_streak += 1
                    best_streak = max(best_streak, current_streak)
                    
                    if puzzle_type == "anagram":
                        anagrams_solved += 1
                    elif puzzle_type == "scramble":
                        scrambles_solved += 1
                    elif puzzle_type == "length":
                        length_puzzles_solved += 1
                else:
                    current_streak = 0

                self.cursor.execute("""
                    UPDATE statistics
                    SET puzzles_solved = ?, puzzles_attempted = ?, anagrams_solved = ?,
                        scrambles_solved = ?, length_puzzles_solved = ?, 
                        current_streak = ?, best_streak = ?
                    WHERE user_id = ?
                """, (puzzles_solved, puzzles_attempted, anagrams_solved, scrambles_solved,
                      length_puzzles_solved, current_streak, best_streak, user_id))
                self.conn.commit()
        except Exception as e:
            logger.error(f"Statistika yenilənərkən xəta: {e}")

    def get_statistics(self, user_id):
        """İstifadəçi statistikalarını qaytarır"""
        try:
            self.cursor.execute("""
                SELECT puzzles_solved, puzzles_attempted, anagrams_solved, scrambles_solved,
                       length_puzzles_solved, current_streak, best_streak
                FROM statistics WHERE user_id = ?
            """, (user_id,))
            return self.cursor.fetchone()
        except Exception as e:
            logger.error(f"Statistika alınarkən xəta: {e}")
            return None

    def get_daily_puzzle_status(self, user_id, puzzle_date=None):
        """Gündəlik tapmaca vəziyyətini qaytarır"""
        try:
            if puzzle_date is None:
                puzzle_date = date.today()
            
            self.cursor.execute("""
                SELECT solved, attempts FROM daily_puzzles
                WHERE user_id = ? AND puzzle_date = ?
            """, (user_id, puzzle_date))
            return self.cursor.fetchone()
        except Exception as e:
            logger.error(f"Gündəlik tapmaca vəziyyəti alınarkən xəta: {e}")
            return None

    def mark_daily_puzzle_solved(self, user_id, puzzle_date=None):
        """Gündəlik tapmacanı həll edildi kimi qeyd edir"""
        try:
            if puzzle_date is None:
                puzzle_date = date.today()
            
            self.cursor.execute("""
                INSERT OR REPLACE INTO daily_puzzles (user_id, puzzle_date, solved, attempts)
                VALUES (?, ?, 1, COALESCE((SELECT attempts FROM daily_puzzles 
                                           WHERE user_id = ? AND puzzle_date = ?), 0) + 1)
            """, (user_id, puzzle_date, user_id, puzzle_date))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Gündəlik tapmaca qeyd edilərkən xəta: {e}")

    def close(self):
        """Verilənlər bazası əlaqəsini bağlayır"""
        self.conn.close()