"""
X-O oyununun məntiqi - oyun vəziyyəti, qalibiyyət yoxlama, AI hərəkəti
"""
import random
import logging

logger = logging.getLogger(__name__)


class TicTacToe:
    def __init__(self):
        """Oyunu başlatır - boş taxta ilə"""
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'  # İstifadəçi X, bot O
        self.moves_count = 0

    def get_board_display(self):
        """Oyun taxtasını emoji ilə gözəl formada göstərir"""
        emoji_map = {
            'X': '❌',
            'O': '⭕',
            ' ': '⬜'
        }
        
        board_str = "┌───┬───┬───┐\n"
        for i, row in enumerate(self.board):
            board_str += "│ "
            board_str += " │ ".join([emoji_map[cell] for cell in row])
            board_str += " │\n"
            if i < 2:
                board_str += "├───┼───┼───┤\n"
        board_str += "└───┴───┴───┘\n"
        board_str += "\n📋 Düymələr: 1-9 nömrələri ilə hərəkət edin"
        return board_str

    def make_move(self, row, col, player):
        """Hərəkət edir - əgər etibarlıdırsa"""
        if self.board[row][col] == ' ':
            self.board[row][col] = player
            self.moves_count += 1
            return True
        return False

    def check_winner(self):
        """Qalibiyyəti yoxlayır"""
        # Sətirləri yoxla
        for row in self.board:
            if row[0] == row[1] == row[2] != ' ':
                return row[0]

        # Sütunları yoxla
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != ' ':
                return self.board[0][col]

        # Diaqonalları yoxla
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return self.board[0][2]

        return None

    def is_board_full(self):
        """Taxta dolu olub olmadığını yoxlayır"""
        return all(cell != ' ' for row in self.board for cell in row)

    def get_game_state(self):
        """Oyun vəziyyətini qaytarır"""
        winner = self.check_winner()
        if winner:
            return 'win' if winner == 'X' else 'lose'
        if self.is_board_full():
            return 'draw'
        return 'playing'

    def get_available_moves(self):
        """Mövcud hərəkətləri qaytarır"""
        moves = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    moves.append((i, j))
        return moves

    def minimax(self, depth, is_maximizing):
        """
        Minimax alqoritmi - AI üçün ən yaxşı hərəkəti tapır
        Bu alqoritm bütün mümkün oyun vəziyyətlərini yoxlayır
        """
        winner = self.check_winner()
        
        if winner == 'O':  # Bot qalib
            return 10 - depth
        if winner == 'X':  # İstifadəçi qalib
            return depth - 10
        if self.is_board_full():  # Heç-heçə
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for move in self.get_available_moves():
                self.board[move[0]][move[1]] = 'O'
                score = self.minimax(depth + 1, False)
                self.board[move[0]][move[1]] = ' '
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for move in self.get_available_moves():
                self.board[move[0]][move[1]] = 'X'
                score = self.minimax(depth + 1, True)
                self.board[move[0]][move[1]] = ' '
                best_score = min(score, best_score)
            return best_score

    def get_best_move(self):
        """AI üçün ən yaxşı hərəkəti tapır"""
        best_score = float('-inf')
        best_move = None

        available_moves = self.get_available_moves()
        if not available_moves:
            return None

        # Bəzən təsadüfi hərəkət et (daha maraqlı oyun üçün)
        if random.random() < 0.1 and len(available_moves) > 1:
            return random.choice(available_moves)

        for move in available_moves:
            self.board[move[0]][move[1]] = 'O'
            score = self.minimax(0, False)
            self.board[move[0]][move[1]] = ' '

            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def reset(self):
        """Oyunu sıfırlayır"""
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.moves_count = 0