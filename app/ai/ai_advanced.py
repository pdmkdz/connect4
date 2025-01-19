__author__= 'Michele DeL Zoppo'
__copyright__='MIT Licence'
__version_number__='1.0.0'

import numpy as np
from typing import Tuple, List, Optional
from PyQt5.QtCore import QTimer


class playerAI():
    def __init__(self, game_instance, player_number: int = 2, depth: int = 4):
        """
        Initialize the AI player
        
        Args:
            game_instance: Instance of the Connect4 GUI game
            player_number: 1 or 2, representing player 1 or 2 (default 2)
            depth: How many moves ahead to look (default 4)
        """
        self.game = game_instance
        self.player_number = player_number
        self.opponent_number = 3 - player_number
        self.depth = depth
        
    def make_ai_move(self):
        """
        Determine and execute the best move for the current board state
        """
        # Get the best move
        move = self.get_move(self.game.board)
        
        # Use a small delay to make the AI move visible
        QTimer.singleShot(500, lambda: self.game.makeMove(move))
        
    def get_move(self, board: np.ndarray) -> int:
        """
        Determine the best move for the current board state
        
        Args:
            board: 6x7 numpy array with 0 for empty, 1 for player 1, 2 for player 2
            
        Returns:
            Column number (0-6) for the best move
        """
        valid_moves = self.get_valid_moves(board)
        if not valid_moves:
            return -1
            
        best_score = float('-inf')
        best_move = valid_moves[0]
        
        for move in valid_moves:
            new_board = board.copy()
            self._make_move(new_board, move, self.player_number)
            score = self._minimax(new_board, self.depth - 1, float('-inf'), float('inf'), False)
            
            if score > best_score:
                best_score = score
                best_move = move
                
        return best_move
    
    def _minimax(self, board: np.ndarray, depth: int, alpha: float, beta: float, maximizing_player: bool) -> float:
        """
        Minimax algorithm with alpha-beta pruning
        """
        if depth == 0 or self._is_terminal_node(board):
            return self._evaluate_position(board)
        
        valid_moves = self.get_valid_moves(board)
        if not valid_moves:
            return 0
        
        if maximizing_player:
            max_eval = float('-inf')
            for move in valid_moves:
                new_board = board.copy()
                self._make_move(new_board, move, self.player_number)
                eval = self._minimax(new_board, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in valid_moves:
                new_board = board.copy()
                self._make_move(new_board, move, self.opponent_number)
                eval = self._minimax(new_board, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval
    
    def _evaluate_position(self, board: np.ndarray) -> float:
        """
        Evaluate the current board position
        """
        score = 0
        
        # Check horizontal, vertical, and diagonal lines
        for window in self._get_windows(board):
            score += self._evaluate_window(window)
            
        # Add extra weight to center column control
        center_array = board[:, 3]
        center_count = np.sum(center_array == self.player_number)
        score += center_count * 3
            
        return score
    
    def _evaluate_window(self, window: np.ndarray) -> float:
        """
        Evaluate a window of 4 positions
        """
        ai_count = np.sum(window == self.player_number)
        opponent_count = np.sum(window == self.opponent_number)
        empty_count = np.sum(window == 0)
        
        if ai_count == 4:
            return 100
        elif ai_count == 3 and empty_count == 1:
            return 5
        elif ai_count == 2 and empty_count == 2:
            return 2
        elif opponent_count == 4:
            return -100
        elif opponent_count == 3 and empty_count == 1:
            return -4
        elif opponent_count == 2 and empty_count == 2:
            return -1
        
        return 0
    
    def _get_windows(self, board: np.ndarray) -> List[np.ndarray]:
        """
        Get all possible windows of 4 positions
        """
        windows = []
        
        # Horizontal windows
        for row in range(6):
            for col in range(4):
                windows.append(board[row, col:col+4])
                
        # Vertical windows
        for row in range(3):
            for col in range(7):
                windows.append(board[row:row+4, col])
                
        # Diagonal windows (positive slope)
        for row in range(3):
            for col in range(4):
                windows.append(np.array([board[row+i, col+i] for i in range(4)]))
                
        # Diagonal windows (negative slope)
        for row in range(3, 6):
            for col in range(4):
                windows.append(np.array([board[row-i, col+i] for i in range(4)]))
                
        return windows
    
    def _is_terminal_node(self, board: np.ndarray) -> bool:
        """
        Check if the current board state is terminal (game over)
        """
        # Check for any valid moves
        if not self.get_valid_moves(board):
            return True
            
        # Check for win
        for window in self._get_windows(board):
            if np.sum(window == self.player_number) == 4 or np.sum(window == self.opponent_number) == 4:
                return True
                
        return False
    
    @staticmethod
    def get_valid_moves(board: np.ndarray) -> List[int]:
        """
        Get list of valid moves for the current board state
        """
        return [col for col in range(7) if board[0, col] == 0]
    
    @staticmethod
    def _make_move(board: np.ndarray, column: int, player: int) -> None:
        """
        Make a move on the board
        """
        for row in range(5, -1, -1):
            if board[row, column] == 0:
                board[row, column] = player
                break
