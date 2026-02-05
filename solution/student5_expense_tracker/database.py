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

        # Xərclər cədvəli
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                amount REAL NOT NULL,
                category TEXT,
                description TEXT,
                expense_date DATE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)

        # Gəlirlər cədvəli
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS income (
                income_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                amount REAL NOT NULL,
                description TEXT,
                income_date DATE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)

        # Büdcələr cədvəli
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS budgets (
                budget_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                category TEXT,
                amount REAL NOT NULL,
                period TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
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
            self.conn.commit()
        except Exception as e:
            logger.error(f"İstifadəçi əlavə edilərkən xəta: {e}")

    def add_expense(self, user_id, amount, category, description, expense_date=None):
        """Xərc əlavə edir"""
        try:
            if expense_date is None:
                expense_date = date.today()
            
            self.cursor.execute("""
                INSERT INTO expenses (user_id, amount, category, description, expense_date)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, amount, category, description, expense_date))
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            logger.error(f"Xərc əlavə edilərkən xəta: {e}")
            return None

    def add_income(self, user_id, amount, description, income_date=None):
        """Gəlir əlavə edir"""
        try:
            if income_date is None:
                income_date = date.today()
            
            self.cursor.execute("""
                INSERT INTO income (user_id, amount, description, income_date)
                VALUES (?, ?, ?, ?)
            """, (user_id, amount, description, income_date))
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            logger.error(f"Gəlir əlavə edilərkən xəta: {e}")
            return None

    def get_expenses(self, user_id, start_date=None, end_date=None, category=None):
        """Xərcləri qaytarır"""
        try:
            query = "SELECT expense_id, amount, category, description, expense_date FROM expenses WHERE user_id = ?"
            params = [user_id]
            
            if start_date:
                query += " AND expense_date >= ?"
                params.append(start_date)
            if end_date:
                query += " AND expense_date <= ?"
                params.append(end_date)
            if category:
                query += " AND category = ?"
                params.append(category)
            
            query += " ORDER BY expense_date DESC"
            
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except Exception as e:
            logger.error(f"Xərclər alınarkən xəta: {e}")
            return []

    def get_income(self, user_id, start_date=None, end_date=None):
        """Gəlirləri qaytarır"""
        try:
            query = "SELECT income_id, amount, description, income_date FROM income WHERE user_id = ?"
            params = [user_id]
            
            if start_date:
                query += " AND income_date >= ?"
                params.append(start_date)
            if end_date:
                query += " AND income_date <= ?"
                params.append(end_date)
            
            query += " ORDER BY income_date DESC"
            
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except Exception as e:
            logger.error(f"Gəlirlər alınarkən xəta: {e}")
            return []

    def get_total_expenses(self, user_id, start_date=None, end_date=None):
        """Ümumi xərcləri hesablayır"""
        try:
            query = "SELECT SUM(amount) FROM expenses WHERE user_id = ?"
            params = [user_id]
            
            if start_date:
                query += " AND expense_date >= ?"
                params.append(start_date)
            if end_date:
                query += " AND expense_date <= ?"
                params.append(end_date)
            
            self.cursor.execute(query, params)
            result = self.cursor.fetchone()
            return result[0] if result[0] else 0.0
        except Exception as e:
            logger.error(f"Ümumi xərclər hesablanarkən xəta: {e}")
            return 0.0

    def get_total_income(self, user_id, start_date=None, end_date=None):
        """Ümumi gəlirləri hesablayır"""
        try:
            query = "SELECT SUM(amount) FROM income WHERE user_id = ?"
            params = [user_id]
            
            if start_date:
                query += " AND income_date >= ?"
                params.append(start_date)
            if end_date:
                query += " AND income_date <= ?"
                params.append(end_date)
            
            self.cursor.execute(query, params)
            result = self.cursor.fetchone()
            return result[0] if result[0] else 0.0
        except Exception as e:
            logger.error(f"Ümumi gəlirlər hesablanarkən xəta: {e}")
            return 0.0

    def set_budget(self, user_id, category, amount, period="monthly"):
        """Büdcə təyin edir"""
        try:
            # Köhnə büdcəni sil
            self.cursor.execute("""
                DELETE FROM budgets WHERE user_id = ? AND category = ? AND period = ?
            """, (user_id, category, period))
            
            # Yeni büdcə əlavə et
            self.cursor.execute("""
                INSERT INTO budgets (user_id, category, amount, period)
                VALUES (?, ?, ?, ?)
            """, (user_id, category, amount, period))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Büdcə təyin edilərkən xəta: {e}")
            return False

    def get_budgets(self, user_id):
        """Büdcələri qaytarır"""
        try:
            self.cursor.execute("""
                SELECT category, amount, period FROM budgets WHERE user_id = ?
            """, (user_id,))
            return self.cursor.fetchall()
        except Exception as e:
            logger.error(f"Büdcələr alınarkən xəta: {e}")
            return []

    def delete_expense(self, expense_id, user_id):
        """Xərci silir"""
        try:
            self.cursor.execute("""
                DELETE FROM expenses WHERE expense_id = ? AND user_id = ?
            """, (expense_id, user_id))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Xərc silinərkən xəta: {e}")
            return False

    def close(self):
        """Verilənlər bazası əlaqəsini bağlayır"""
        self.conn.close()