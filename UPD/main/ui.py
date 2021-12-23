from typing import Awaitable
from PySide6.QtWidgets import QApplication, QHBoxLayout, QLineEdit, QSizePolicy, QWidget, QMainWindow, QPushButton, QLabel, QVBoxLayout, QVBoxLayout, QScrollArea
from PySide6.QtCore import Property, QPropertyAnimation, QPoint, QEasingCurve, QRect, Qt
from PySide6.QtGui import QBrush, QFont, QPainter, QPen
from PySide6 import QtWidgets

from extension.utils import get_tools
from upd.ui import Console, MainPanel, RLineEdit, Navigator


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
        try:
            self.centralWidget().load()
        except:
            pass


class LoadingScreen(MainPanel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = QLabel('UPD', self)
        self.label.setText('UPD')
        self.console = Console('Loading assets...<br> initializing ui...<font color="rgb(0, 0, 0)">text</font>')

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


    def load(self):
        from main.tool import tool
        tools = [tool]
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
        self.parent().navigate(Desk(self.parent()))

    def paintEvent(self, e):
        from main import settings
        super().paintEvent(e)
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

        painter.end()


class Desk(MainPanel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = QHBoxLayout()
        self.setLayout(layout)
        self.navigator = Navigator(self)
        self.navigator.setGeometry(100, 100, 200, 400)
        self.navigator.on_select(self.navigate)

        for tool in get_tools():
            self.navigator.add_option(tool.get_icon(), tool.get_name(), tool)

    def navigate(self ,tool):
        self.parent().navigate(tool.get_main_panel())
