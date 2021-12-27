from PySide6.QtWidgets import QPushButton, QScrollArea, QVBoxLayout
from PySide6.QtCore import QRect, Qt
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

    def add_project(self):
        Project.create()

    def paintEvent(self, e):
        geometry = QRect(self.shrink, self.rect().bottomRight()-self.shrink)
        self.grid.setGeometry(geometry)
        super().paintEvent(e)


class GraphCanvas(RWidget):
    def __init__(self):
        self.nodes = []
        self.relations = []
        self.data = []
        self.graph = None


    def get_data(self):
        self.nodes = Node.filter(Node.graph==self.graph)
        return 

    def refresh_data():
        pass

    def refresh():
        pass
