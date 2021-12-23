from PySide6.QtWidgets import QPushButton, QVBoxLayout
from PySide6.QtCore import QRect
from .tool import tool
from .models import Drawer

from upd.ui import MainPanel, RLineEdit, RGridView

@tool.main_panel
class FileCabinetPanel(MainPanel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid = RGridView(self)
        self.grid.bind_model(Drawer, name='name', description='description')
        self.grid.on_create(self.add_drawer)

    def add_drawer(self):
        Drawer.create()

    def paintEvent(self, e):
        geometry = QRect(self.shrink, self.rect().bottomRight()-self.shrink)
        self.grid.setGeometry(geometry)
        super().paintEvent(e)
