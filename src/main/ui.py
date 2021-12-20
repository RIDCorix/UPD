from typing import Awaitable
from PySide6.QtWidgets import QApplication, QSizePolicy, QWidget, QMainWindow, QPushButton, QLabel, QVBoxLayout, QVBoxLayout, QScrollArea
from PySide6.QtCore import Property, QPropertyAnimation, QPoint, QEasingCurve, QRect, Qt
from PySide6.QtGui import QBrush, QFont, QPainter, QPen
from PySide6 import QtWidgets

from core.utils import slide
from core.ui import RWidget, Console

from main import settings

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(1000, 600)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowTitle("My App")

        # Set the central widget of the Window.
        self.navigate(LoadingScreen())

    def navigate(self, widget: QWidget):
        widget.resize(self.size()*9/10)
        self.setCentralWidget(widget)

    def load(self):
        self.centralWidget().load()


class LoadingScreen(RWidget):
    def get_drop_rate(self):
        return self._drop_rate


    def set_drop_rate(self,val):
        self._drop_rate = val
        self.update()

    drop_rate = Property(float, get_drop_rate, set_drop_rate)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._drop_rate = 0
        self.label = QLabel('UPD', self)
        self.label.setText('UPD')
        self.console = Console('Loading assets...<br> initializing ui...<font color="rgb(0, 0, 0)">text</font>')


        effect = QtWidgets.QGraphicsDropShadowEffect(self)
        effect.setOffset(0, 0)
        effect.setBlurRadius(20)
        self.setGraphicsEffect(effect)

        effect = QtWidgets.QGraphicsOpacityEffect(self.console)
        effect.setOpacity(0.1)
        self.console.setGraphicsEffect(effect)
        self.console.setFont(QFont('Share Tech Mono', 10))
        self.console.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.console.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.console.setWordWrap(True)

        self.console_area = QScrollArea(self)
        self.console_area.setWidget(self.console)
        self.console_area.setProperty('hidden', 'True')
        self.console_area.setStyleSheet("background-color:transparent;")
        self.console_area.setFixedSize(600, 200)
        self.console_area.setWidgetResizable(True)
        bar = self.console_area.verticalScrollBar()
        bar.rangeChanged.connect( lambda x,y: bar.setValue(y) )


        effect = QtWidgets.QGraphicsOpacityEffect(self.label)
        effect.setOpacity(0.1)
        self.label.setGraphicsEffect(effect)
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.label.setFont(QFont('Share Tech Mono', 60))
        self.label.setMinimumSize(300, 200)
        self.loaded = False
        self.setProperty('type', 'panel')


    def load(self):
        import importlib
        from main.tool import tool
        tools = [tool]
        QApplication.processEvents()
        with self.console.block() as block:
            for i, tool in enumerate(tools):
                done = i+1
                total = len(tools)
                block.progress(f'Initializing...{tool}', done, total)
                for i, task in enumerate(tool.init_tasks):
                    with block.block() as task_block:
                        done = i+1
                        total = len(tool.init_tasks)
                        block.progress(f'{task}', done, total)
                        with block.block() as task_block:
                            task(tool, console=task_block)
        self.console.line('Complete')
        self.slide('drop_rate', 1.0, 0.0, callback='pulled')

    def pulled(self):
        print('pulled')

    def paintEvent(self, e):
        super().paintEvent(e)
        self.update()
        self.console.update()
        center = self.rect().center()
        width = self.rect().width()
        height = self.rect().height()

        self.label.move(center - QPoint(0, 50+height * (1-self.drop_rate) / 20) - self.label.rect().center())
        self.console_area.move(center + QPoint(0, 150+height * (1-self.drop_rate) / 20) - self.console_area.rect().center())

        if self.drop_rate < 1:
            self.label.graphicsEffect().setOpacity(self.drop_rate)
            self.console.graphicsEffect().setOpacity(self.drop_rate)

        painter = QPainter()
        painter.begin(self)
        painter.setPen(QPen(settings.BORDER_COLOR, 2))
        painter.drawLine(center - QPoint(width * self.drop_rate / 5, 0), center + QPoint(width * self.drop_rate / 5, 0))


        painter.drawRect(self.rect())
        painter.setPen(QPen(settings.BORDER_COLOR, 0))
        painter.setBrush(QBrush(settings.PANEL_COLOR))
        rect = self.rect()
        size = rect.bottomRight()
        rect = QRect(size/20, size*19/20)
        painter.drawRect(rect)
        painter.end()
