from typing import Any

from PySide6.QtCore import Property, QPropertyAnimation, QPoint, QEasingCurve, Qt
from PySide6.QtWidgets import QWidget, QMainWindow, QPushButton



def slide(obj: QWidget, att: str, from_value: Any, to_value: Any, duration: int=500):
    obj.anim = QPropertyAnimation(obj, b"pos")
    obj.anim.setStartValue(from_value)
    obj.anim.setEndValue(to_value)
    obj.anim.setDuration(duration)
    obj.anim.start()
