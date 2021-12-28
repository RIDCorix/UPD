from PySide6 import QtCore
from PySide6.QtGui import QAction, QBrush, QColor, QPainter, QPen
from PySide6.QtWidgets import QMenu, QPushButton, QScrollArea, QVBoxLayout
from PySide6.QtCore import QPoint, QRect, QSize, Qt
from .tool import tool
from .models import Project

from upd.ui import MainPanel, RLineEdit, RGridView, RWidget

from .models import Node, Relation


@tool.main_panel
class UsPanel(MainPanel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid = RGridView(self)
        self.grid.bind_model(Project, name='name', description='description')
        self.grid.on_create(self.add_project)
        self.grid.on_select(lambda data: self.parent().navigate(GraphCanvas(data)))

    def add_project(self):
        Project.create()

    def paintEvent(self, e):
        geometry = QRect(self.shrink, self.rect().bottomRight()-self.shrink)
        self.grid.setGeometry(geometry)
        super().paintEvent(e)


class GraphCanvas(RWidget):
    def __init__(self, data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.graph_id = data['id']
        self.nodes = []
        self.relations = []
        self.data = []
        self.graph = None

        self.add_node_menu = QMenu(self)
        self.add_node_menu.addAction('hello', self.add_node)
        GraphNode(self)

    def add_node(self):
        print(self.sender())

    def mousePressEvent(self, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == QtCore.Qt.RightButton:
                self.add_node_menu.move(self.parent().pos() + event.pos())
                self.add_node_menu.exec()
            else:
                super().mousePressEvent(event)

    def get_data(self):
        self.nodes = Node.filter(Node.graph==self.graph)
        pass

    def refresh_data():
        pass

    def refresh():
        pass


class GraphNode(MainPanel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slide('size', QSize(0, 0), QSize(300, 200))

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.slide('size', to_value=QSize(400, 600))

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.slide('size', to_value=QSize(300, 200))

    def enterEvent(self, event):
        super().enterEvent(event)
        self.slide('size', to_value=QSize(400, 600))

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.slide('size', to_value=QSize(300, 200))
