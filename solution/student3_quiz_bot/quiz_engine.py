"""
Viktorina mühərriki - oyun məntiqi və idarəetmə
"""
import logging
from questions import get_questions, get_categories

logger = logging.getLogger(__name__)


class QuizEngine:
    def __init__(self):
        """Viktorina mühərriki obyektini yaradır"""
        self.current_quiz = None
        self.user_quizzes = {}  # {user_id: quiz_data}

    def start_quiz(self, user_id, category):
        """Yeni viktorina başladır"""
        questions = get_questions(category, 10)
        if not questions:
            return None
        
        quiz_data = {
            "category": category,
            "questions": questions,
            "current_question": 0,
            "score": 0,
            "answers": []
        }
        
        self.user_quizzes[user_id] = quiz_data
        return quiz_data

    def get_current_question(self, user_id):
        """Cari sualı qaytarır"""
        if user_id not in self.user_quizzes:
            return None
        
        quiz = self.user_quizzes[user_id]
        if quiz["current_question"] >= len(quiz["questions"]):
            return None
        
        return quiz["questions"][quiz["current_question"]]

    def answer_question(self, user_id, answer_index):
        """Suala cavab verir"""
        if user_id not in self.user_quizzes:
            return None
        
        quiz = self.user_quizzes[user_id]
        current_q = quiz["questions"][quiz["current_question"]]
        
        is_correct = (answer_index == current_q["correct"])
        
        if is_correct:
            quiz["score"] += 1
        
        quiz["answers"].append({
            "question": current_q["question"],
            "user_answer": answer_index,
            "correct_answer": current_q["correct"],
            "is_correct": is_correct
        })
        
        quiz["current_question"] += 1
        
        return {
            "is_correct": is_correct,
            "correct_answer": current_q["correct"],
            "score": quiz["score"],
            "total": len(quiz["questions"]),
            "current": quiz["current_question"]
        }

    def is_finished(self, user_id):
        """Oyun bitib bitmədiyini yoxlayır"""
        if user_id not in self.user_quizzes:
            return True
        
        quiz = self.user_quizzes[user_id]
        return quiz["current_question"] >= len(quiz["questions"])

    def get_results(self, user_id):
        """Oyun nəticələrini qaytarır"""
        if user_id not in self.user_quizzes:
            return None
        
        quiz = self.user_quizzes[user_id]
        score = quiz["score"]
        total = len(quiz["questions"])
        percentage = (score / total * 100) if total > 0 else 0
        
        return {
            "category": quiz["category"],
            "score": score,
            "total": total,
            "percentage": percentage,
            "answers": quiz["answers"]
        }

    def end_quiz(self, user_id):
        """Oyunu bitirir və məlumatları silir"""
        results = self.get_results(user_id)
        if user_id in self.user_quizzes:
            del self.user_quizzes[user_id]
        return results

    def format_question(self, question_data, question_num, total):
        """Sualı formatlaşdırır"""
        text = f"❓ Sual {question_num}/{total}\n\n"
        text += f"{question_data['question']}\n\n"
        
        options_emoji = ["A", "B", "C", "D"]
        for i, option in enumerate(question_data['options']):
            text += f"{options_emoji[i]}) {option}\n"
        
        return text