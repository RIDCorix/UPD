from PySide6.QtWidgets import QVBoxLayout
from .tool import tool

from upd.ui import MainPanel, RLineEdit, RGridView

@tool.main_panel
class FileCabinetPanel(MainPanel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.grid = RGridView()
        layout.addWidget(self.grid)
