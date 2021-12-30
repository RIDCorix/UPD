from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6.QtGui import QAction, QBrush, QColor, QIcon, QPainter, QPen, QPixmap, QTransform
from PySide6.QtWidgets import QCheckBox, QGraphicsItem, QGraphicsScene, QGraphicsWidget, QHBoxLayout, QLabel, QMenu, QMenuBar, QPushButton, QScrollArea, QVBoxLayout, QWidget
from PySide6.QtCore import Property, QPoint, QRect, QSize, Qt
from .tool import tool
from .models import Project, Connection, Node

from upd.ui import MainPanel, RLineEdit, RGridView, RWidget, RButton



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
        self.connecting = False
        self.connecting_from = None

        self.always_show_title = QCheckBox('Always Show Title', self)

        self.offset = QPoint(0, 0)
        self.scale = 1

        self.dragging = False
        self.dragging_from = QPoint(0, 0)

        self.graph_id = data['id']

        self.nodes = {}
        self.connections = {}

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

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Alt:
            self.connecting = not self.connecting
            for item in self.nodes.values():
                if self.connecting:
                    item.slide('connector_rate', to_value=1)
                    item.connector.show()
                else:
                    item.slide('connector_rate', to_value=0, callback=lambda:item.connector.hide())

        return super().keyPressEvent(event)

    def add_node(self):
        Node.create(x=self.mouse_pos.x(), y=self.mouse_pos.y(), graph_id=self.graph_id)
        self.refresh_data()

    def create_connection(self, to_id):
        if self.connecting_from == to_id:
            return
        else:
            Connection.create(from_node_id=self.connecting_from, to_node_id=to_id)
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
                if not self.dragging_node_id:
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
        self.node_data = Node.select(Node.id, Node.name, Node.x, Node.y).where(Node.removed==False).dicts()
        from_alias = Node.alias()
        to_alias = Node.alias()
        self.connection_data = list(
            Connection.select(Connection.type, Connection.id, Connection.from_node, Connection.to_node)
            .where(Connection.removed==False)
            .join(from_alias, on=Connection.from_node)
            .where(from_alias.removed==False)
            .switch(Connection)
            .join(to_alias, on=Connection.to_node)
            .where(to_alias.removed==False)
            .dicts()
        )

    def refresh_data(self):
        self.get_data()
        self.refresh()

    def refresh(self):
        items_to_remove = list(self.nodes.keys())
        for item in self.node_data:
            if item['id'] not in self.nodes:
                node = GraphNode(item, self)
                node.show()
                self.nodes[item['id']] = node

            pos = QPoint(item['x'], item['y'])
            self.nodes[item['id']].slide('pos', to_value=pos + self.offset)
            self.nodes[item['id']].update_data(item)
            try:
                items_to_remove.remove(item['id'])
            except:
                pass

        for node_id in items_to_remove:
            node = self.nodes[node_id]
            node.removed=True
            node.slide('size', to_value=QSize(0, 0))

        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter()
        painter.begin(self)
        painter.setPen(QColor(255, 255, 255))
        for item in self.connection_data:
            if item['id'] not in self.connections:
                from_node = self.nodes[item['from_node']]
                to_node = self.nodes[item['to_node']]

            from_point = from_node.pos() + from_node.rect().center()
            to_point = to_node.pos() + to_node.rect().center()
            painter.drawLine(from_point, to_point)

        painter.end()


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
    def get_connector_rate(self):
        return self._connector_rate

    def set_connector_rate(self,val):
        self._connector_rate = val
        self.update()

    connector_rate = Property(float, get_connector_rate, set_connector_rate)

    def __init__(self, data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._connector_rate = 0

        self.SIZE_MINIMAL = QSize(50, 50)
        self.SIZE_WIDE = QSize(400, 50)
        self.SIZE_FULL = QSize(400, 600)
        self.removed = False

        self.slide('size', QSize(0, 0), self.SIZE_MINIMAL)
        self.data = data

        self.label = NodeTitle(self, self.data['name'])
        self.label.textChanged.connect(self.rename)

        self.header = RWidget(self)
        self.header_layout = QHBoxLayout()
        self.header.setLayout(self.header_layout)

        self.icon = RButton(QPixmap('assets/file-cabinet/icon.png'), '')
        self.icon.setFixedSize(30, 30)

        self.remove_button = RButton('x')
        self.remove_button.setFixedSize(30, 30)
        self.remove_button.clicked.connect(self.remove)

        self.header_layout.addWidget(self.icon)
        self.header_layout.addWidget(self.label)
        self.header_layout.addWidget(self.remove_button)

        self.connector = RButton('+', self.parent())
        self.connector.clicked.connect(lambda:self._connect(self.data['id']))
        self.connector.hide()
        self.header.move(0, 0)
        self.header.update()

    def _connect(self, node_id):
        if self.parent().connecting_from:
            self.parent().create_connection(node_id)
            self.parent().connecting_from = None
        else:
            self.parent().connecting_from = node_id


    def remove(self):
        Node.update(removed=True).where(Node.id==self.data['id']).execute()
        self.parent().refresh_data()
        self.parent().refresh()

    def rename(self, e):
        Node.update(name=self.label.text()).where(Node.id==self.data['id']).execute()
        text_width = len(self.label.text())*10
        self.SIZE_WIDE.setWidth(max(text_width + 100, 200))
        self.slide('size', to_value=self.SIZE_WIDE)

    def update_data(self, data):
        self.data = data

    def paintEvent(self, *args, **kwargs):
        self.connector.setStyleSheet(f'background-color: rgba(255, 255, 255, {self.connector_rate});color: rgba(0, 0, 0, {self.connector_rate});')
        if not self.removed:
            self.parent().update()
            super().paintEvent(*args, **kwargs)
            self.header.setFixedWidth(max(self.size().width(), 150))
            self.header.slide('size', to_value=QSize(self.size().width(), 50))
            self.connector.move(self.pos()+self.rect().center()-self.connector.rect().center() + QPoint(0, -50*self.connector_rate))

    def mousePressEvent(self, event):
        if not self.removed:
            if event.button() == QtCore.Qt.LeftButton:
                self.parent().dragging_node_id = self.data['id']
                self.parent().dragging_node_from = event.pos() + self.pos()

    def mouseReleaseEvent(self, event):
        if not self.removed:
            if event.button() == QtCore.Qt.LeftButton:
                self.parent().dragging_node_id = None

    def enterEvent(self, event):
        super().enterEvent(event)
        if not self.removed:
            self.slide('size', to_value=self.SIZE_WIDE)

    def leaveEvent(self, event):
        super().leaveEvent(event)
        if not self.removed:
            if not self.label.hasFocus():
                if not self.parent().always_show_title.isChecked():
                    self.slide('size', to_value=self.SIZE_MINIMAL)
