from PySide6 import QtCore
from PySide6.QtGui import QAction, QBrush, QColor, QPainter, QPen
from PySide6.QtWidgets import QGraphicsItem, QGraphicsScene, QGraphicsWidget, QLabel, QMenu, QPushButton, QScrollArea, QVBoxLayout
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


class GraphCanvas(MainPanel):
    def __init__(self, data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scene = QGraphicsScene()
        self.graph_id = data['id']
        self.nodes = {}

        self.node_data = []
        self.connection_data = []

        self.relations = []
        self.graph = None

        self.mouse_pos = QPoint(0, 0)

        self.add_node_menu = QMenu(self)
        self.add_node_menu.addAction('hello', self.add_node)
        self.refresh_data()

    def add_node(self):
        Node.create(x=self.mouse_pos.x(), y=self.mouse_pos.y(), graph_id=self.graph_id)
        self.refresh_data()

    def mousePressEvent(self, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == QtCore.Qt.RightButton:
                self.mouse_pos = event.pos()
                self.add_node_menu.move(self.mouse_pos+self.parent().pos())
                self.add_node_menu.exec()
            else:
                super().mousePressEvent(event)

    def get_data(self):
        self.node_data = Node.select(Node.id, Node.name, Node.x, Node.y).dicts()

    def refresh_data(self):
        self.get_data()
        self.refresh()

    def refresh(self):
        for item in self.node_data:
            if item['id'] not in self.nodes:
                pos = QPoint(item['x'], item['y'])
                node = GraphNode(item, self)
                node.show()
                node.slide('pos', to_value=pos)
                self.nodes[item['id']] = node
                self.scene.addItem(node)

            self.nodes[item['id']].update_data(item)


class RNode(QGraphicsWidget):
    def paintEvent(self, e):
        super().paintEvent(e)

        painter = QPainter()
        painter.begin(self)
        painter.setPen(QPen(QColor(255, 255, 255), 2))

        painter.drawRect(self.rect())
        painter.setPen(QPen(QColor(255, 255, 255), 0))
        painter.setBrush(QBrush(QColor(0, 0, 0, 100)))
        rect = self.rect()
        size = rect.bottomRight()
        short = min(rect.width(), rect.height())
        self.shrink = QPoint(short, short) / 20
        rect = QRect(self.shrink, size-self.shrink)
        painter.drawRect(rect)
        painter.end()


class GraphNode(MainPanel, QGraphicsWidget):

    SIZE_MINIMAL = QSize(50, 50)
    SIZE_WIDE = QSize(400, 50)
    SIZE_FULL = QSize(400, 600)

    def __init__(self, data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slide('size', QSize(0, 0), self.SIZE_MINIMAL)
        self.data = data
        self.label = RLineEdit('A Task')
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

    def update_data(self, data):
        self.data = data

    def mousePressEvent(self, event):
        self.slide('size', to_value=self.SIZE_FULL)

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.slide('size', to_value=self.SIZE_WIDE)

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.slide('size', to_value=self.SIZE_MINIMAL)

    def enterEvent(self, event):
        super().enterEvent(event)
        self.slide('size', to_value=self.SIZE_WIDE)

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.slide('size', to_value=self.SIZE_MINIMAL)
