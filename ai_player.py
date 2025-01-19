__author__= 'Michele DeL Zoppo'
__copyright__='MIT Licence'
__version_number__='1.0.0'

import numpy as np
from typing import Tuple, List, Optional
from PyQt5.QtCore import QTimer

class randomAI():
    def __init__(self, game_instance, player_number: int = 2, depth: int = 4):
        """
        Initialize the random AI player
        
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

