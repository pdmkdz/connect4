__author__= 'Michele DeL Zoppo'
__copyright__='Unlicense'
__version_number__='1.0.0'

import os
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
        
        

