from PySide6.QtWidgets import QApplication, QWidget

from main.ui import MainWindow, LoadingScreen

import sys

app = QApplication(sys.argv)

window = LoadingScreen()
window.show()

app.exec_()
