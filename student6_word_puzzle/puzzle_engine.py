"""
Söz tapmacası mühərriki - anagram, söz yarışması və digər oyunlar

TODO:
1. AnagramSolver sinfi - get_anagrams, generate_anagram_puzzle
2. WordScramble sinfi - generate_scramble
3. WordLengthPuzzle sinfi - generate_puzzle
4. DailyPuzzle sinfi - generate_daily_puzzle (seed ilə)
"""

# TODO: Import-ları əlavə edin
# from collections import Counter
# from word_database import get_random_word, is_valid_word, get_words_by_length
# import random


class AnagramSolver:
    @staticmethod
    def get_anagrams(letters):
        """
        Verilən hərflərdən anagramlar tapır
        
        TODO:
        1. letters.lower() et
        2. Counter(letters) ilə hərflərin sayını hesabla
        3. WORDS_DATABASE-dəki hər sözü yoxla
        4. Sözün hərfləri verilən hərflərdə varmı yoxla
        5. Uyğun sözləri qaytar (uzunluğa görə sırala)
        """
        # TODO: Anagram alqoritmi
        return []

    @staticmethod
    def generate_anagram_puzzle():
        """
        Anagram tapmacası yaradır
        
        TODO:
        1. Söz seç
        2. Hərfləri qarışdır
        3. Dictionary qaytar: {"scrambled": ..., "answer": ..., "hint": ...}
        """
        # TODO: Anagram tapmacası
        return {}


class WordScramble:
    @staticmethod
    def generate_scramble():
        """
        Söz yarışması yaradır
        
        TODO:
        1. Söz seç (5-10 hərf)
        2. Hərfləri qarışdır
        3. Dictionary qaytar
        """
        # TODO: Söz yarışması
        return {}


class WordLengthPuzzle:
    @staticmethod
    def generate_puzzle():
        """
        Söz uzunluğu tapmacası yaradır
        
        TODO:
        1. Uzunluq seç (4-10)
        2. Həmin uzunluqda söz seç
        3. Bəzi hərfləri aç (məsələn 2 hərf)
        4. Qalanları "_" ilə gizlət
        5. Dictionary qaytar
        """
        # TODO: Uzunluq tapmacası
        return None


class DailyPuzzle:
    @staticmethod
    def generate_daily_puzzle(seed=None):
        """
        Gündəlik tapmaca yaradır (seed ilə eyni gün üçün eyni tapmaca)
        
        TODO:
        1. seed yoxdursa: date.today().toordinal() istifadə et
        2. random.seed(seed) çağır
        3. Təsadüfi tapmaca növü seç
        4. Uyğun sinifin generate funksiyasını çağır
        5. Dictionary qaytar
        """
        # TODO: Gündəlik tapmaca
        return {}


def check_word_match(user_word, correct_word):
    """
    İstifadəçi sözünün düzgün olub olmadığını yoxlayır
    
    TODO:
    1. Hər iki sözü lower() et
    2. strip() et
    3. Müqayisə et
    """
    # TODO: Söz müqayisəsi
    return False