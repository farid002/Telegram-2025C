"""
Vərdiş idarəetməsi - vərdişlərlə işləmə məntiqi
"""
import logging
from datetime import datetime, date, timedelta
from database import Database

logger = logging.getLogger(__name__)


class HabitManager:
    def __init__(self, db: Database):
        """Vərdiş idarəetməsi obyektini yaradır"""
        self.db = db

    def add_habit(self, user_id, habit_name, emoji="✅"):
        """Yeni vərdiş əlavə edir"""
        return self.db.add_habit(user_id, habit_name, emoji)

    def delete_habit(self, habit_id, user_id):
        """Vərdişi silir"""
        return self.db.delete_habit(habit_id, user_id)

    def get_user_habits(self, user_id):
        """İstifadəçinin vərdişlərini qaytarır"""
        return self.db.get_habits(user_id)

    def checkin_habit(self, habit_id, checkin_date=None):
        """Vərdiş üçün qeydiyyat edir"""
        return self.db.checkin_habit(habit_id, checkin_date)

    def get_habit_stats(self, habit_id):
        """Vərdiş statistikalarını qaytarır"""
        checkins = self.db.get_checkins(habit_id)
        streak = self.db.get_streak(habit_id)
        
        today = date.today()
        this_month = self.db.get_monthly_stats(habit_id, today.year, today.month)
        
        # Son 7 gün
        week_ago = today - timedelta(days=7)
        recent_checkins = [c for c in checkins if isinstance(c, str) and date.fromisoformat(c) >= week_ago or (isinstance(c, date) and c >= week_ago)]
        week_count = len(recent_checkins)
        
        # Son 30 gün
        month_ago = today - timedelta(days=30)
        month_checkins = [c for c in checkins if isinstance(c, str) and date.fromisoformat(c) >= month_ago or (isinstance(c, date) and c >= month_ago)]
        month_count = len(month_checkins)
        
        total_count = len(checkins)
        
        return {
            'streak': streak,
            'total': total_count,
            'this_month': this_month,
            'week': week_count,
            'month': month_count
        }

    def format_habits_list(self, habits):
        """Vərdişlər siyahısını formatlaşdırır"""
        if not habits:
            return "📝 Hələ heç bir vərdiş əlavə etməmisiniz."
        
        text = "📋 Sizin Vərdişləriniz:\n\n"
        for habit_id, habit_name, emoji in habits:
            stats = self.get_habit_stats(habit_id)
            text += f"{emoji} {habit_name}\n"
            text += f"   🔥 Streak: {stats['streak']} gün | 📊 Cəmi: {stats['total']} qeydiyyat\n\n"
        
        return text