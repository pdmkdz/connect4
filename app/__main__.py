__author__= 'Michele DeL Zoppo'
__copyright__='Unlicense'
__version_number__='1.0.0'

import sys
import os
import numpy as np
from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QMessageBox
from PyQt5.QtGui import QMovie
from ai.ai_player import randomAI

class Connect4(QDialog):
    def __init__(self):
        super().__init__() # inerith from QDialog
        uic.loadUi(os.path.join(os.getcwd(), 'app/assets/connect4GUI.ui'), self) # load UI file, which is easier to work with than building from code
        self.gameMode = None

        # init dictionary with color pattern for players
        self.colorPattern = {'current': {
            1: self.p1color.currentText(),
            2: self.p2color.currentText() 
        },
        'previous': {
            1: self.p1color.currentText(),
            2: self.p2color.currentText() 
        }}

        self.ai = randomAI(self)
        self.startGUI()

    def startGUI(self):
        self.setWindowTitle(f'Connect 4 - v{__version_number__}')

        self.numRows = 6
        self.numCols = 7

        self.board = np.zeros((self.numRows, self.numCols), int) # this makes up the data point for the board
        self.currentPlayer = 1
        
        self.reset_button.clicked.connect(lambda: self.resetGame())

        self.p1color.activated.connect(lambda: self.recolorBoard(1))
        self.p2color.activated.connect(lambda: self.recolorBoard(2))

        self.human_ai.stateChanged.connect(lambda: self.updateGameMode())

        self.updateGameMode() #set initial state by reading checkmark

        self.movie = QMovie(os.path.join(os.getcwd(), "app/assets/Connect_Four.gif"))
        self.movie.start()

        self.ai_turn.setMovie(self.movie)
        self.ai_turn.setScaledContents(True)
        self.ai_turn.hide()

        self.buttons = []
        for row in range(self.numRows):
            rowButtons = []
            for col in range(self.numCols):
                button = QPushButton('')
                button.setFixedSize(70, 70)
                button.setStyleSheet('''
                    QPushButton {
                        border-radius: 35px;
                        background-color: white;
                        border: 2px solid black;
                    }
                ''')
                button.clicked.connect(lambda _, c=col: self.if_ai_move(c))
                self.gridLayout.addWidget(button, row, col)
                rowButtons.append(button)
            self.buttons.append(rowButtons)

        self.show()

    def if_ai_move(self, col):
        """Checks game mode and makes moves accordingly.

        Args:
            col (int): column where to place move.
        """
        if self.gameMode == '2 players':
            self.makeMove(col)
        else:
            self.makeMove(col)
            self.ai.make_ai_move()

    def makeMove(self, col):
        """Makes a move in Connect 4, placing the current player's piece in the specified column.

        Checks for a win and switches to the other player if the game continues.
        """
        # Find the lowest available row in the column
        for r in range(self.numRows - 1, -1, -1):
            if self.board[r, col] == 0:
                self.board[r, col] = self.currentPlayer
                self.updateButtonColor(r, col)
                result = self.checkWin(r, col)
                if result == True:
                    self.gameOver()
                else:
                    self.currentPlayer = 3 - self.currentPlayer  # Switch player (1 or 2)
                break
        self.ai_turn.hide()

    def updateButtonColor(self, row, col):
        """Updates the color of the cell selected based on player count.
        Red for player 1 and blue for player 2.

        Args:
            row (_type_): _description_
            col (_type_): _description_
        """
        self.buttons[row][col].setStyleSheet(f'''
                QPushButton {{
                    border-radius: 35px;
                    background-color: {self.colorPattern['current'][self.board[row, col]]};
                    border: 2px solid black;
                }}
            ''')

    def checkWin(self, row, col):
        """
        Checks if the current player has won the game by forming a line of 4
        starting from the specified (row, col) position.
        """
        # Directions: horizontal, vertical, diagonal (/), diagonal (\)
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 1  # Include the current position
            
            # Check in the positive direction (dr, dc)
            for step in range(1, 4):
                r, c = row + step * dr, col + step * dc
                if 0 <= r < self.numRows and 0 <= c < self.numCols and self.board[r][c] == self.currentPlayer:
                    count += 1
                else:
                    break
            
            # Check in the negative direction (-dr, -dc)
            for step in range(1, 4):
                r, c = row - step * dr, col - step * dc
                if 0 <= r < self.numRows and 0 <= c < self.numCols and self.board[r][c] == self.currentPlayer:
                    count += 1
                else:
                    break
            
            # Check if we found 4 in a row
            if count >= 4:
                return True
        
        return False

    def gameOver(self):
        print(f"Player {self.currentPlayer} wins!")

        msg = QMessageBox()
        # msg.setIcon(QMessageBox.Warning)
        msg.setWindowIcon(QtGui.QIcon('Connect_Four.gif'))
        msg.setText(
            f'<div style="text-align: center;">'
            f'<h3>Player {self.currentPlayer} wins!</h3>'
            f'<br><br>'
            f'<img src="app/assets/win4.png" width="100" height="100">'
            f'</div>'
        )
        msg.setWindowTitle('GAME OVER!')
        msg.setStandardButtons(QMessageBox.Ok)
        msg.raise_()
        msg.exec_()

        self.close()
        self.__init__()

    def resetGame(self):
        self.close()
        self.__init__()

    def updateGameMode(self):
        if self.human_ai.isChecked():
            self.gameMode = '2 players'
        else:
            self.gameMode = 'vs ai'
        
        print(f'Game Mode Set: {self.gameMode}')

    def recolorBoard(self, player):
        """Recolor Board when selecting new color for player. 

        Args:
            player (str): player set either 1 or 2
        """

        self.colorPattern['previous'][player] = self.colorPattern['current'][player]
        if player == 1:
            self.colorPattern['current'][player] = self.p1color.currentText()
        else:
           self.colorPattern['current'][player] = self.p2color.currentText()

        # Iterate across the board to check for colors and recolor
        for row in range(self.numRows):
            for col in range(self.numCols):
                value = self.buttons[row][col].styleSheet()
                if self.colorPattern['previous'][player] in value:
                    self.buttons[row][col].setStyleSheet(f'''
                                                         QPushButton {{
                                                         border-radius: 35px;
                                                         background-color: {self.colorPattern['current'][self.board[row, col]]};
                                                         border: 2px solid black;
                                                         }}
                                                         ''')


            

        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Connect4()
    sys.exit(app.exec_())