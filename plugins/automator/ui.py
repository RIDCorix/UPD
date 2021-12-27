from PySide6.QtWidgets import QPushButton, QScrollArea, QVBoxLayout
from PySide6.QtCore import QRect, Qt
from .tool import tool
from .models import Script

from upd.ui import MainPanel, RLineEdit, RGridView

@tool.main_panel
class AutomatorPanel(MainPanel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid = RGridView(self)
        self.grid.setGeometry(self.geometry())
        self.grid.bind_model(Script, name='name', description='description')
        self.grid.on_create(self.add_drawer)

    def add_drawer(self):
        Script.create()

    def paintEvent(self, e):
        geometry = QRect(self.shrink, self.rect().bottomRight()-self.shrink)
        self.grid.setGeometry(geometry)
        super().paintEvent(e)
