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

        # Vərdişlər cədvəli
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS habits (
                habit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                habit_name TEXT NOT NULL,
                emoji TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)

        # Gündəlik qeydiyyatlar cədvəli
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS checkins (
                checkin_id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER,
                checkin_date DATE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (habit_id) REFERENCES habits(habit_id),
                UNIQUE(habit_id, checkin_date)
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
            self.conn.commit()
        except Exception as e:
            logger.error(f"İstifadəçi əlavə edilərkən xəta: {e}")

    def add_habit(self, user_id, habit_name, emoji="✅"):
        """Yeni vərdiş əlavə edir"""
        try:
            self.cursor.execute("""
                INSERT INTO habits (user_id, habit_name, emoji)
                VALUES (?, ?, ?)
            """, (user_id, habit_name, emoji))
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            logger.error(f"Vərdiş əlavə edilərkən xəta: {e}")
            return None

    def delete_habit(self, habit_id, user_id):
        """Vərdişi silir"""
        try:
            self.cursor.execute("""
                DELETE FROM habits WHERE habit_id = ? AND user_id = ?
            """, (habit_id, user_id))
            self.cursor.execute("""
                DELETE FROM checkins WHERE habit_id = ?
            """, (habit_id,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Vərdiş silinərkən xəta: {e}")
            return False

    def get_habits(self, user_id):
        """İstifadəçinin bütün vərdişlərini qaytarır"""
        try:
            self.cursor.execute("""
                SELECT habit_id, habit_name, emoji
                FROM habits WHERE user_id = ?
                ORDER BY created_at DESC
            """, (user_id,))
            return self.cursor.fetchall()
        except Exception as e:
            logger.error(f"Vərdişlər alınarkən xəta: {e}")
            return []

    def checkin_habit(self, habit_id, checkin_date=None):
        """Vərdiş üçün gündəlik qeydiyyat edir"""
        try:
            if checkin_date is None:
                checkin_date = date.today()
            
            self.cursor.execute("""
                INSERT OR IGNORE INTO checkins (habit_id, checkin_date)
                VALUES (?, ?)
            """, (habit_id, checkin_date))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Qeydiyyat edilərkən xəta: {e}")
            return False

    def get_checkins(self, habit_id, start_date=None, end_date=None):
        """Vərdiş üçün qeydiyyatları qaytarır"""
        try:
            if start_date and end_date:
                self.cursor.execute("""
                    SELECT checkin_date FROM checkins
                    WHERE habit_id = ? AND checkin_date BETWEEN ? AND ?
                    ORDER BY checkin_date
                """, (habit_id, start_date, end_date))
            else:
                self.cursor.execute("""
                    SELECT checkin_date FROM checkins
                    WHERE habit_id = ?
                    ORDER BY checkin_date DESC
                """, (habit_id,))
            return [row[0] for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Qeydiyyatlar alınarkən xəta: {e}")
            return []

    def get_streak(self, habit_id):
        """Vərdiş üçün cari streak-i hesablayır"""
        try:
            checkins = self.get_checkins(habit_id)
            if not checkins:
                return 0
            
            today = date.today()
            streak = 0
            current_date = today
            
            # Tarixləri sırala
            checkin_dates = sorted([date.fromisoformat(c) if isinstance(c, str) else c for c in checkins], reverse=True)
            
            for checkin_date in checkin_dates:
                if isinstance(checkin_date, str):
                    checkin_date = date.fromisoformat(checkin_date)
                
                if checkin_date == current_date or checkin_date == current_date:
                    streak += 1
                    current_date = date(current_date.year, current_date.month, current_date.day - 1)
                else:
                    break
            
            return streak
        except Exception as e:
            logger.error(f"Streak hesablanarkən xəta: {e}")
            return 0

    def get_monthly_stats(self, habit_id, year, month):
        """Aylıq statistika qaytarır"""
        try:
            start_date = date(year, month, 1)
            if month == 12:
                end_date = date(year + 1, 1, 1)
            else:
                end_date = date(year, month + 1, 1)
            
            checkins = self.get_checkins(habit_id, start_date, end_date)
            return len(checkins)
        except Exception as e:
            logger.error(f"Aylıq statistika alınarkən xəta: {e}")
            return 0

    def close(self):
        """Verilənlər bazası əlaqəsini bağlayır"""
        self.conn.close()