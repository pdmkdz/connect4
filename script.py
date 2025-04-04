from connect4app.__main__ import *
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Connect4()
    sys.exit(app.exec_())