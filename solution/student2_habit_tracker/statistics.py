"""
Statistika hesablamaları və formatlaşdırma
"""
import logging
from datetime import date, timedelta
from database import Database

logger = logging.getLogger(__name__)


class Statistics:
    def __init__(self, db: Database):
        """Statistika obyektini yaradır"""
        self.db = db

    def get_calendar_view(self, habit_id, year, month):
        """Aylıq təqvim görünüşü yaradır"""
        try:
            start_date = date(year, month, 1)
            if month == 12:
                end_date = date(year + 1, 1, 1)
            else:
                end_date = date(year, month + 1, 1)
            
            checkins = self.db.get_checkins(habit_id, start_date, end_date)
            checkin_dates = set()
            for c in checkins:
                if isinstance(c, str):
                    checkin_dates.add(date.fromisoformat(c))
                else:
                    checkin_dates.add(c)
            
            # Təqvim yaradır
            calendar = []
            first_day = start_date
            first_weekday = first_day.weekday()
            
            # Həftə günləri başlığı
            weekdays = ["B", "B.e", "Ç.a", "Ç", "C.a", "C", "Ş"]
            
            # Boş günlər
            for _ in range(first_weekday):
                calendar.append("  ")
            
            # Günlər
            current_date = start_date
            while current_date < end_date:
                if current_date in checkin_dates:
                    calendar.append("✅")
                else:
                    calendar.append("⬜")
                current_date += timedelta(days=1)
            
            # Formatlaşdırma
            month_names = ["Yanvar", "Fevral", "Mart", "Aprel", "May", "İyun",
                          "İyul", "Avqust", "Sentyabr", "Oktyabr", "Noyabr", "Dekabr"]
            
            text = f"📅 {month_names[month-1]} {year}\n\n"
            text += " ".join(weekdays) + "\n"
            
            for i, day in enumerate(calendar):
                text += day + " "
                if (i + 1) % 7 == 0:
                    text += "\n"
            
            return text
        except Exception as e:
            logger.error(f"Təqvim görünüşü yaradılarkən xəta: {e}")
            return "❌ Xəta baş verdi."

    def get_weekly_report(self, user_id):
        """Həftəlik hesabat yaradır"""
        try:
            habits = self.db.get_habits(user_id)
            if not habits:
                return "📊 Hələ heç bir vərdiş yoxdur."
            
            today = date.today()
            week_ago = today - timedelta(days=7)
            
            text = f"📊 Həftəlik Hesabat ({week_ago} - {today})\n\n"
            
            for habit_id, habit_name, emoji in habits:
                checkins = self.db.get_checkins(habit_id, week_ago, today)
                count = len(checkins)
                streak = self.db.get_streak(habit_id)
                
                text += f"{emoji} {habit_name}\n"
                text += f"   ✅ Bu həftə: {count}/7 gün\n"
                text += f"   🔥 Streak: {streak} gün\n\n"
            
            return text
        except Exception as e:
            logger.error(f"Həftəlik hesabat yaradılarkən xəta: {e}")
            return "❌ Xəta baş verdi."