from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6.QtGui import QAction, QBrush, QColor, QIcon, QPainter, QPen, QPixmap, QTransform
from PySide6.QtWidgets import QCheckBox, QGraphicsItem, QGraphicsScene, QGraphicsWidget, QHBoxLayout, QLabel, QMenu, QMenuBar, QPushButton, QScrollArea, QVBoxLayout, QWidget
from PySide6.QtCore import QPoint, QRect, QSize, Qt
from .tool import tool
from .models import Project

from upd.ui import MainPanel, RLineEdit, RGridView, RWidget, RButton

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
        self.always_show_title = QCheckBox('Always Show Title', self)

        self.offset = QPoint(0, 0)
        self.scale = 1

        self.dragging = False
        self.dragging_from = QPoint(0, 0)

        self.graph_id = data['id']
        self.nodes = {}

        self.node_data = []
        self.connection_data = []

        self.dragging_node_id = None
        self.dragging_node_from = None

        self.relations = []
        self.graph = None

        self.mouse_pos = QPoint(0, 0)

        self.add_node_menu = QMenu(self)
        self.add_node_menu.addAction('hello', self.add_node)
        self.refresh_data()

    def add_node(self):
        Node.create(x=self.mouse_pos.x(), y=self.mouse_pos.y(), graph_id=self.graph_id)
        self.refresh_data()

    def mouseMoveEvent(self, event):
        if self.dragging_node_id:
            for item in self.node_data:
                if item['id'] == self.dragging_node_id:
                    delta = event.pos() - self.dragging_node_from
                    item['x'] += delta.x()
                    item['y'] += delta.y()
                    Node.update(x=item['x'], y=item['y']).where(Node.id==item['id']).execute()

                    self.dragging_node_from = event.pos()
            self.refresh()

        elif self.dragging:
            self.offset += event.pos() - self.dragging_from
            self.dragging_from = event.pos()
            self.refresh()

    def mousePressEvent(self, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == QtCore.Qt.RightButton:
                self.mouse_pos = event.pos()
                self.add_node_menu.move(self.mouse_pos+self.parent().pos())
                self.mouse_pos -= self.offset
                self.add_node_menu.exec()
            elif event.button() == QtCore.Qt.LeftButton:
                self.dragging = True
                self.dragging_from = event.pos()
            else:
                super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == QtCore.Qt.LeftButton:
                self.dragging = False
                self.dragging_node_id = None
                self.refresh()
            else:
                super().mouseReleaseEvent(event)

    def get_data(self):
        self.node_data = Node.select(Node.id, Node.name, Node.x, Node.y).dicts()

    def refresh_data(self):
        self.get_data()
        self.refresh()

    def refresh(self):
        for item in self.node_data:
            if item['id'] not in self.nodes:
                node = GraphNode(item, self)
                node.show()
                self.nodes[item['id']] = node

            pos = QPoint(item['x'], item['y'])
            self.nodes[item['id']].slide('pos', to_value=pos + self.offset)
            self.nodes[item['id']].update_data(item)


class NodeTitle(RLineEdit):
    def __init__(self, node, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.node = node

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.node.slide('size', to_value=self.node.SIZE_WIDE)

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        if not self.node.parent().always_show_title.isChecked():
            self.node.slide('size', to_value=self.node.SIZE_MINIMAL)


class GraphNode(MainPanel):

    def __init__(self, data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.SIZE_MINIMAL = QSize(50, 50)
        self.SIZE_WIDE = QSize(400, 50)
        self.SIZE_FULL = QSize(400, 600)

        self.slide('size', QSize(0, 0), self.SIZE_MINIMAL)
        self.data = data
        self.label = NodeTitle(self, self.data['name'])
        self.label.textChanged.connect(self.rename)
        self.header = RWidget(self)
        self.header_layout = QHBoxLayout()
        self.header.setLayout(self.header_layout)
        self.icon = RButton(QPixmap('assets/file-cabinet/icon.png'), '')
        self.icon.setFixedSize(30, 30)
        self.header_layout.addWidget(self.icon)
        self.header_layout.addWidget(self.label)

        self.header.move(0, 0)

    def rename(self, e):
        Node.update(name=self.label.text()).where(Node.id==self.data['id']).execute()
        self.slide('size', to_value=self.SIZE_WIDE)

    def update_data(self, data):
        self.data = data

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        size = self.header.size()
        size.setWidth(len(self.label.text())*10 + 100)
        self.header.slide('size', to_value=size)
        self.SIZE_WIDE.setWidth(len(self.label.text())*10 + 100)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.parent().dragging_node_id = self.data['id']
            self.parent().dragging_node_from = event.pos() + self.pos() - self.parent().pos()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.parent().dragging_node_id = None

    def enterEvent(self, event):
        super().enterEvent(event)
        self.slide('size', to_value=self.SIZE_WIDE)

    def leaveEvent(self, event):
        super().leaveEvent(event)
        if not self.label.hasFocus():
            if not self.parent().always_show_title.isChecked():
                self.slide('size', to_value=self.SIZE_MINIMAL)
