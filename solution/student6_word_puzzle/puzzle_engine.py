"""
Söz tapmacası mühərriki - anagram, söz yarışması və digər oyunlar
"""
import logging
import random
from collections import Counter
from word_database import get_random_word, is_valid_word, get_words_by_length

logger = logging.getLogger(__name__)


class AnagramSolver:
    """Anagram həlledici"""
    
    @staticmethod
    def get_anagrams(letters):
        """Verilən hərflərdən anagramlar tapır"""
        letters = letters.lower().replace(" ", "")
        letter_count = Counter(letters)
        words = get_words_by_length()
        anagrams = []
        
        for word in words:
            word_lower = word.lower()
            word_count = Counter(word_lower)
            
            # Bütün hərflər mövcuddurmu yoxla
            if all(word_count[char] <= letter_count.get(char, 0) for char in word_count):
                anagrams.append(word)
        
        return sorted(anagrams, key=len, reverse=True)
    
    @staticmethod
    def generate_anagram_puzzle():
        """Anagram tapmacası yaradır"""
        word = get_random_word(4, 8)
        letters = list(word)
        random.shuffle(letters)
        scrambled = "".join(letters)
        return {
            "scrambled": scrambled.upper(),
            "answer": word.upper(),
            "hint": f"Söz {len(word)} hərfdən ibarətdir"
        }


class WordLengthPuzzle:
    """Söz uzunluğu tapmacası"""
    
    @staticmethod
    def generate_puzzle():
        """Söz uzunluğu tapmacası yaradır"""
        length = random.randint(4, 10)
        words = get_words_by_length(length, length)
        if not words:
            return None
        
        word = random.choice(words)
        hint_letters = list(word)
        revealed = random.sample(hint_letters, min(2, len(hint_letters)))
        
        display = []
        for char in word:
            if char in revealed:
                display.append(char)
            else:
                display.append("_")
        
        return {
            "display": " ".join(display),
            "answer": word.upper(),
            "length": length,
            "hint": f"Söz {length} hərfdən ibarətdir"
        }


class WordScramble:
    """Söz yarışması (scramble)"""
    
    @staticmethod
    def generate_scramble():
        """Söz yarışması yaradır"""
        word = get_random_word(5, 10)
        letters = list(word)
        random.shuffle(letters)
        scrambled = "".join(letters)
        
        return {
            "scrambled": scrambled.upper(),
            "answer": word.upper(),
            "hint": f"Uzunluq: {len(word)} hərf"
        }


class DailyPuzzle:
    """Gündəlik tapmaca"""
    
    @staticmethod
    def generate_daily_puzzle(seed=None):
        """Gündəlik tapmaca yaradır (seed ilə eyni gün üçün eyni tapmaca)"""
        if seed is None:
            from datetime import date
            seed = date.today().toordinal()
        
        random.seed(seed)
        puzzle_type = random.choice(["anagram", "scramble", "length"])
        
        if puzzle_type == "anagram":
            puzzle = AnagramSolver.generate_anagram_puzzle()
            puzzle["type"] = "anagram"
        elif puzzle_type == "scramble":
            puzzle = WordScramble.generate_scramble()
            puzzle["type"] = "scramble"
        else:
            puzzle = WordLengthPuzzle.generate_puzzle()
            puzzle["type"] = "length"
        
        return puzzle


def check_word_match(user_word, correct_word):
    """İstifadəçi sözünün düzgün olub olmadığını yoxlayır"""
    return user_word.lower().strip() == correct_word.lower().strip()