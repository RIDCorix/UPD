from PySide6.QtWidgets import QWidget, QMainWindow, QPushButton, QLabel, QVBoxLayout
from PySide6.QtCore import Property, QPropertyAnimation, QPoint, QEasingCurve, Qt
from PySide6.QtGui import QPainter

from core.utils import slide

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        button = QPushButton("Press Me!")

        # Set the central widget of the Window.
        self.setCentralWidget(button)


class LoadingScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 600)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.drop_rate = 0

        self.setWindowTitle("My App")
        self.label = QLabel('BRUH')

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)

        slide(self, 'pos', QPoint(0, 0), QPoint(100, 100))

    def paintEvent(self, e):

        painter = QPainter()
        painter.begin(self)
        painter.setPen(Qt.red)

        painter.drawLine(QPoint(0, 0), QPoint(100, 100))
        painter.end()
