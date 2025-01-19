__author__= 'Michele DeL Zoppo'
__copyright__='MIT Licence'
__version_number__='1.0.0'

import sys
import os
import numpy as np
from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QMessageBox

class Connect4(QDialog):
    def __init__(self):
        super().__init__() # inerith from QDialog
        uic.loadUi(os.path.join(os.getcwd(), 'connect4GUI.ui'), self) # load UI file, which is easier to work with than building from code
        self.gameMode = None
        self.startGUI()

    def startGUI(self):
        self.setWindowTitle(f'Connect 4 - v{__version_number__}')

        self.numRows = 6
        self.numCols = 7

        self.board = np.zeros((self.numRows, self.numCols), int)
        self.currentPlayer = 1
        
        self.reset_button.clicked.connect(lambda: self.resetGame())

        self.human_pc.stateChanged.connect(self.updateGameMode)

        self.updateGameMode()

        self.buttons = []
        for row in range(self.numRows):
            rowButtons = []
            for col in range(self.numCols):
                button = QPushButton('')
                button.setFixedSize(60, 60)
                button.clicked.connect(lambda _, c=col: self.makeMove(c))
                self.gridLayout.addWidget(button, row, col)
                rowButtons.append(button)
            self.buttons.append(rowButtons)

        self.show()

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

    def updateButtonColor(self, row, col):
        """Updates the color of the cell selected based on player count.
        Red for player 1 and blue for player 2.

        Args:
            row (_type_): _description_
            col (_type_): _description_
        """
        if self.board[row, col] == 1:
            self.buttons[row][col].setStyleSheet("background-color: green")
        elif self.board[row, col] == 2:
            self.buttons[row][col].setStyleSheet("background-color: yellow")

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
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowIcon(QtGui.QIcon('Connect_Four.gif'))
        msg.setText(f'<h3>Player {self.currentPlayer} wins!</h3>'
                    f'<img src="Connect_Four.gif" width="100" height="100">')
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
        if self.human_pc.isChecked():
            self.gameMode = 'human'
        else:
            self.gameMode = 'ai'
        
        print(f'Game Mode Set: {self.gameMode}')

    # TODO: Add computer player logic

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Connect4()
    sys.exit(app.exec_())