__author__= 'Michele DeL Zoppo'
__copyright__='Unlicense'
__version_number__='1.0.0'

import random
from PyQt5.QtCore import QTimer

# TODO: Get all avaiable moves and choose the best for winning or stopping other player
# TODO: define algorithm to make AI stronger (like looking ahead), did some research and minmax algorithm may be a good one to use

class randomAI():
    def __init__(self, game_istance = None):
        """
        Initialize the random AI player
        
        Args:
            game_instance: Instance of the Connect4 GUI game
        """
        self.game = game_istance

    def make_ai_move(self):
        """
        Get a random move and play it on the board.
        """
        # Get a random move
        random_move = random.randint(0, 6)

        self.game.ai_turn.show()
        # make move like human and switch player
        QTimer.singleShot(700, 
                          lambda: self.game.makeMove(random_move))
        
class smartAI(randomAI):
    def __init__(self, game_instance=None):
        """
        Initialize the smart AI player
        
        Args:
            game_instance: Instance of the Connect4 GUI game
        """
        super().__init__(game_instance)

    def evaluate_window(self, window, piece):
        """
        Evaluate a window of 4 cells for scoring.
        
        Args:
            window: List of 4 cells to evaluate
            piece: The AI's piece (1 or 2)
        
        Returns:
            Score for the window
        """
        score = 0
        opponent_piece = 1 if piece == 2 else 2

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(0) == 1:
            score += 10
        elif window.count(piece) == 2 and window.count(0) == 2:
            score += 5

        if window.count(opponent_piece) == 3 and window.count(0) == 1:
            score -= 80

        return score

    def score_position(self, board, piece):
        """
        Score the board position for the AI.
        
        Args:
            board: Current board state
            piece: The AI's piece (1 or 2)
        
        Returns:
            Total score for the board
        """
        score = 0

        # Score center column
        center_array = [board[row][self.game.numCols // 2] for row in range(self.game.numRows)]
        center_count = center_array.count(piece)
        score += center_count * 6

        # Score horizontal
        for row in range(self.game.numRows):
            row_array = [board[row][col] for col in range(self.game.numCols)]
            for col in range(self.game.numCols - 3):
                window = row_array[col:col + 4]
                score += self.evaluate_window(window, piece)

        # Score vertical
        for col in range(self.game.numCols):
            col_array = [board[row][col] for row in range(self.game.numRows)]
            for row in range(self.game.numRows - 3):
                window = col_array[row:row + 4]
                score += self.evaluate_window(window, piece)

        # Score positive diagonal
        for row in range(self.game.numRows - 3):
            for col in range(self.game.numCols - 3):
                window = [board[row + i][col + i] for i in range(4)]
                score += self.evaluate_window(window, piece)

        # Score negative diagonal
        for row in range(self.game.numRows - 3):
            for col in range(self.game.numCols - 3):
                window = [board[row + 3 - i][col + i] for i in range(4)]
                score += self.evaluate_window(window, piece)

        return score

    def get_valid_locations(self, board):
        """
        Get all valid column indices where a move can be made.
        
        Args:
            board: Current board state
        
        Returns:
            List of valid column indices
        """
        return [col for col in range(self.game.numCols) if board[0][col] == 0]

    def pick_best_move(self, board, piece):
        """
        Pick the best move for the AI based on scoring.
        
        Args:
            board: Current board state
            piece: The AI's piece (1 or 2)
        
        Returns:
            Best column index for the move
        """
        valid_locations = self.get_valid_locations(board)
        best_score = -float('inf')
        best_col = random.choice(valid_locations)

        for col in valid_locations:
            row = next(r for r in range(self.game.numRows - 1, -1, -1) if board[r][col] == 0)
            temp_board = board.copy()
            temp_board[row][col] = piece
            score = self.score_position(temp_board, piece)
            if score > best_score:
                best_score = score
                best_col = col

        return best_col

    def make_ai_move(self):
        """
        Make a move using the smart AI algorithm.
        """
        best_move = self.pick_best_move(self.game.board, 2)  # Assuming AI is player 2
        self.game.ai_turn.show()
        QTimer.singleShot(700, 
                            lambda: self.game.makeMove(best_move))

