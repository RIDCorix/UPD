from PySide6.QtCore import QFile, QTextStream
from PySide6.QtWidgets import QApplication, QWidget

import sys
import threading

app = QApplication(sys.argv)
from main.ui import MainWindow

window = MainWindow()
window.show()
from main import settings
print(settings.to_dict())
rendered = open("stylesheet/normal.qss", "r").read().format(**settings.to_dict())

app.setStyleSheet(rendered)
t = threading.Thread(target=window.load)
t.start()
app.exec()
