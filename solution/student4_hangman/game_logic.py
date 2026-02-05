"""
Adam Asma oyununun məntiqi
"""
import logging
from config import MAX_WRONG_GUESSES

logger = logging.getLogger(__name__)


class HangmanGame:
    def __init__(self, word):
        """Oyunu başlatır"""
        self.word = word.upper()
        self.guessed_letters = set()
        self.wrong_guesses = 0
        self.max_wrong = MAX_WRONG_GUESSES
        self.game_over = False
        self.won = False

    def guess_letter(self, letter):
        """Hərf təxmin edir"""
        letter = letter.upper()
        
        if letter in self.guessed_letters:
            return {"status": "already_guessed", "message": "Bu hərfi artıq təxmin etmisiniz!"}
        
        self.guessed_letters.add(letter)
        
        if letter in self.word:
            # Düzgün təxmin
            if self.is_word_complete():
                self.won = True
                self.game_over = True
                return {"status": "won", "message": "🎉 Təbriklər! Sözü tapdınız!"}
            return {"status": "correct", "message": "✅ Düzgün hərf!"}
        else:
            # Səhv təxmin
            self.wrong_guesses += 1
            if self.wrong_guesses >= self.max_wrong:
                self.game_over = True
                return {"status": "lost", "message": f"😔 Oyun bitdi! Söz: {self.word}"}
            return {"status": "wrong", "message": f"❌ Səhv! Qalan cəhd: {self.max_wrong - self.wrong_guesses}"}

    def get_display_word(self):
        """Sözü gizli formada göstərir"""
        display = []
        for char in self.word:
            if char in self.guessed_letters:
                display.append(char)
            else:
                display.append("_")
        return " ".join(display)

    def is_word_complete(self):
        """Söz tam tapılıbmı yoxlayır"""
        return all(char in self.guessed_letters for char in self.word)

    def get_hangman_display(self):
        """Adamın vəziyyətini vizual göstərir"""
        stages = [
            """
               --------
               |      |
               |
               |
               |
               |
            =========
            """,
            """
               --------
               |      |
               |      O
               |
               |
               |
            =========
            """,
            """
               --------
               |      |
               |      O
               |      |
               |
               |
            =========
            """,
            """
               --------
               |      |
               |      O
               |     /|
               |
               |
            =========
            """,
            """
               --------
               |      |
               |      O
               |     /|\\
               |
               |
            =========
            """,
            """
               --------
               |      |
               |      O
               |     /|\\
               |     /
               |
            =========
            """,
            """
               --------
               |      |
               |      O
               |     /|\\
               |     / \\
               |
            =========
            """
        ]
        
        return stages[min(self.wrong_guesses, len(stages) - 1)]

    def get_status(self):
        """Oyun vəziyyətini qaytarır"""
        return {
            "display_word": self.get_display_word(),
            "wrong_guesses": self.wrong_guesses,
            "max_wrong": self.max_wrong,
            "guessed_letters": sorted(self.guessed_letters),
            "game_over": self.game_over,
            "won": self.won,
            "word": self.word if self.game_over else None
        }