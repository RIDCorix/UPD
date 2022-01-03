from PySide6.QtCore import QFile, QTextStream
from PySide6.QtWidgets import QApplication, QWidget


import sys
import threading

from extension.utils import get_tools
from peewee import *

get_tools()
from file_cabinet.models import Drawer

app = QApplication(sys.argv)
from main.ui import MainWindow
from main.settings import tool
window = MainWindow()
window.show()
from upd.conf import settings
rendered = open("stylesheet/normal.qss", "r").read().format(**settings.to_dict())

app.setStyleSheet(rendered)
t = threading.Thread(target=window.load)
t.start()
sys.exit(app.exec())

