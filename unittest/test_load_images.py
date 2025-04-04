import unittest
import os
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtGui import QMovie, QPixmap
from PyQt5.uic import loadUi

# Ensure a QApplication instance exists
app = QApplication([])

class TestLoadAssets(unittest.TestCase):
    def setUp(self):
        # Define paths to assets
        self.ui_path = "connect4app/assets/connect4GUI.ui"
        self.gif_path = "connect4app/assets/Connect_Four.gif"
        self.png_path = "connect4app/assets/win4.png"

    def test_load_ui_file(self):
        """Test loading the .ui file."""
        self.assertTrue(os.path.exists(self.ui_path), f"{self.ui_path} does not exist")
        try:
            window = QDialog()
            loadUi(self.ui_path, window)
        except Exception as e:
            self.fail(f"Failed to load .ui file: {e}")

    def test_load_gif_file(self):
        """Test loading the .gif file as a QMovie."""
        self.assertTrue(os.path.exists(self.gif_path), f"{self.gif_path} does not exist")
        try:
            movie = QMovie(self.gif_path)
            self.assertTrue(movie.isValid(), "Failed to load .gif file as QMovie")
        except Exception as e:
            self.fail(f"Failed to load .gif file: {e}")

    def test_load_png_file(self):
        """Test loading the .png file as a QPixmap."""
        self.assertTrue(os.path.exists(self.png_path), f"{self.png_path} does not exist")
        try:
            pixmap = QPixmap(self.png_path)
            self.assertFalse(pixmap.isNull(), "Failed to load .png file as QPixmap")
        except Exception as e:
            self.fail(f"Failed to load .png file: {e}")

if __name__ == "__main__":
    unittest.main()