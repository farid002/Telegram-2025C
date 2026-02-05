"""
Viktorina mühərriki - oyun məntiqi və idarəetmə

TODO:
1. QuizEngine sinfi yaradın
2. start_quiz, get_current_question, answer_question, is_finished, get_results funksiyaları
"""

# TODO: Import-ları əlavə edin
# from questions import get_questions


class QuizEngine:
    def __init__(self):
        """
        Viktorina mühərriki obyektini yaradır
        
        TODO:
        1. user_quizzes = {}  # {user_id: quiz_data}
        """
        # TODO: Init
        pass

    def start_quiz(self, user_id, category):
        """
        Yeni viktorina başladır
        
        TODO:
        1. get_questions() ilə sualları al
        2. quiz_data yarat: {"category": ..., "questions": ..., "current_question": 0, "score": 0, "answers": []}
        3. user_quizzes[user_id] = quiz_data
        """
        # TODO: Viktorina başlatma
        return None

    def get_current_question(self, user_id):
        """Cari sualı qaytarır"""
        # TODO: Cari sual alma
        return None

    def answer_question(self, user_id, answer_index):
        """
        Suala cavab verir
        
        TODO:
        1. Cari sualı al
        2. Düzgün cavabı yoxla
        3. Düzgündürsə: score += 1
        4. answers list-inə əlavə et
        5. current_question += 1
        6. Nəticə dictionary qaytar: {"is_correct": ..., "score": ..., "current": ...}
        """
        # TODO: Cavab vermə
        return None

    def is_finished(self, user_id):
        """Oyun bitib bitmədiyini yoxlayır"""
        # TODO: Oyun bitmə yoxlama
        return False

    def get_results(self, user_id):
        """
        Oyun nəticələrini qaytarır
        
        TODO:
        1. quiz_data-dan score, total hesabla
        2. Faiz hesabla: (score / total) * 100
        3. Dictionary qaytar
        """
        # TODO: Nəticə hesablama
        return None

    def end_quiz(self, user_id):
        """Oyunu bitirir və məlumatları silir"""
        # TODO: Oyun bitirmə
        return None

    def format_question(self, question_data, question_num, total):
        """
        Sualı formatlaşdırır
        
        TODO:
        1. "❓ Sual X/Y" formatında başlıq
        2. Sual mətni
        3. Seçimlər: "A) ...", "B) ...", və s.
        4. String qaytar
        """
        # TODO: Sual formatlaşdırma
        return ""