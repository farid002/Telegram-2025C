"""
Adam Asma oyununun məntiqi

TODO:
1. HangmanGame sinfi yaradın
2. guess_letter, get_display_word, check_winner, get_hangman_display funksiyaları
"""

# TODO: Import-ları əlavə edin
# from config import MAX_WRONG_GUESSES


class HangmanGame:
    def __init__(self, word):
        """
        Oyunu başlatır
        
        TODO:
        1. self.word = word.upper()
        2. self.guessed_letters = set()
        3. self.wrong_guesses = 0
        4. self.max_wrong = MAX_WRONG_GUESSES
        5. self.game_over = False
        6. self.won = False
        """
        # TODO: Init kodunu yazın
        pass

    def guess_letter(self, letter):
        """
        Hərf təxmin edir
        
        TODO:
        1. letter.upper() et
        2. Artıq təxmin edilibsə: "already_guessed" qaytar
        3. guessed_letters-ə əlavə et
        4. Düzgün hərfdirsə: "correct" qaytar, is_word_complete() yoxla
        5. Səhv hərfdirsə: wrong_guesses += 1, "wrong" qaytar
        6. Oyun bitibsə: "won" və ya "lost" qaytar
        """
        # TODO: Hərf təxmin etmə
        return {"status": "wrong", "message": ""}

    def get_display_word(self):
        """
        Sözü gizli formada göstərir
        
        TODO:
        1. Hər hərf üçün: guessed_letters-də varsa hərf, yoxdursa "_"
        2. " ".join() ilə birləşdir
        """
        # TODO: Söz göstərmə
        return ""

    def is_word_complete(self):
        """Söz tam tapılıbmı yoxlayır"""
        # TODO: Bütün hərflər təxmin edilibmi yoxla
        return False

    def get_hangman_display(self):
        """
        Adamın vəziyyətini vizual göstərir
        
        TODO:
        1. 7 mərhələli ASCII art yaradın
        2. wrong_guesses-ə görə uyğun mərhələni qaytar
        """
        # TODO: Vizual göstərici
        return ""

    def get_status(self):
        """
        Oyun vəziyyətini qaytarır
        
        TODO:
        1. Dictionary qaytar: display_word, wrong_guesses, guessed_letters, game_over, won
        2. Oyun bitibsə, word də əlavə et
        """
        # TODO: Vəziyyət qaytarma
        return {}