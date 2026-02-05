"""
X-O oyununun məntiqi - oyun vəziyyəti, qalibiyyət yoxlama, AI hərəkəti

Bu faylı tamamlamaq üçün:
1. TicTacToe sinfi yaradın
2. Oyun taxtası və vəziyyət idarəetməsi
3. Minimax alqoritmi ilə AI hərəkəti
"""

# TODO: Import-ları əlavə edin
# import random
# import logging
# from config import MAX_WRONG_GUESSES  # Bu fayl üçün lazım deyil, amma nümunədir

# logger = logging.getLogger(__name__)


class TicTacToe:
    def __init__(self):
        """
        Oyunu başlatır - boş taxta ilə
        
        TODO:
        1. 3x3 boş taxta yaradın (list of lists)
        2. current_player = 'X' (istifadəçi)
        3. moves_count = 0
        """
        # TODO: Oyun taxtasını və vəziyyəti yaradın
        # self.board = [[' ' for _ in range(3)] for _ in range(3)]
        # self.current_player = 'X'
        # self.moves_count = 0
        pass

    def get_board_display(self):
        """
        Oyun taxtasını emoji ilə gözəl formada göstərir
        
        TODO:
        1. Emoji map yaradın: {'X': '❌', 'O': '⭕', ' ': '⬜'}
        2. Taxtanı formatlaşdırın (sətirlər, sütunlar)
        3. String qaytarın
        """
        # TODO: Taxta göstərmə kodunu yazın
        return ""

    def make_move(self, row, col, player):
        """
        Hərəkət edir - əgər etibarlıdırsa
        
        TODO:
        1. Taxta[row][col] boşdursa, hərəkət et
        2. moves_count artır
        3. True/False qaytar
        """
        # TODO: Hərəkət etmə kodunu yazın
        return False

    def check_winner(self):
        """
        Qalibiyyəti yoxlayır
        
        TODO:
        1. Sətirləri yoxla (3 eyni hərf)
        2. Sütunları yoxla
        3. Diaqonalları yoxla
        4. Qalib varsa, hərfi qaytar ('X' və ya 'O')
        5. Yoxdursa, None qaytar
        """
        # TODO: Qalibiyyət yoxlama kodunu yazın
        return None

    def is_board_full(self):
        """
        Taxta dolu olub olmadığını yoxlayır
        
        TODO:
        1. Bütün xanaların dolu olub olmadığını yoxla
        2. True/False qaytar
        """
        # TODO: Taxta dolu yoxlama kodunu yazın
        return False

    def get_game_state(self):
        """
        Oyun vəziyyətini qaytarır
        
        TODO:
        1. check_winner() çağır
        2. Qalib varsa: 'win' (istifadəçi) və ya 'lose' (bot)
        3. Taxta doludursa: 'draw'
        4. Davam edirsə: 'playing'
        """
        # TODO: Oyun vəziyyəti kodunu yazın
        return 'playing'

    def get_available_moves(self):
        """
        Mövcud hərəkətləri qaytarır
        
        TODO:
        1. Boş xanaları tap
        2. (row, col) tuple-ları list kimi qaytar
        """
        # TODO: Mövcud hərəkətlər kodunu yazın
        return []

    def minimax(self, depth, is_maximizing):
        """
        Minimax alqoritmi - AI üçün ən yaxşı hərəkəti tapır
        
        TODO:
        1. Oyun bitibsə, xal qaytar (bot qalib: +10, istifadəçi qalib: -10, heç-heçə: 0)
        2. is_maximizing True-dursa (bot):
           - Bütün mümkün hərəkətləri yoxla
           - Hər hərəkət üçün minimax çağır (rekursiv)
           - Maksimum xalı qaytar
        3. is_maximizing False-dursa (istifadəçi):
           - Minimum xalı qaytar
        
        İpucu: Bu rekursiv funksiyadır. Dərinlik artdıqca xal azalır.
        """
        # TODO: Minimax alqoritmini yazın
        return 0

    def get_best_move(self):
        """
        AI üçün ən yaxşı hərəkəti tapır
        
        TODO:
        1. Mövcud hərəkətləri al
        2. Hər hərəkət üçün minimax çağır
        3. Ən yüksək xalı olan hərəkəti qaytar
        4. (row, col) tuple qaytar
        """
        # TODO: Ən yaxşı hərəkət tapma kodunu yazın
        return None

    def reset(self):
        """Oyunu sıfırlayır"""
        # TODO: Taxta və vəziyyəti sıfırlayın
        pass