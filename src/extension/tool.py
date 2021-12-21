import abc
from importlib import import_module

from PySide6.QtGui import QPixmap

class Tool(metaclass=abc.ABCMeta):
    def __init__(self, *args, **kwargs):
        self.init_tasks = []
        self.settings = {}

    def init_task(self, task_function):
        self.init_tasks.append(task_function)

    def get_icon(self):
        return QPixmap(f'assets/{self.get_name()}/icon.png')

    def get_name(self):
        return 'unnamed-tool'

class ToolSettings:
    def __init__(self, ):
        import_module()