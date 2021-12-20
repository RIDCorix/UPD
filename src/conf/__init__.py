import importlib
import pkgutil
from PySide6.QtCore import QSettings


class GlobalSettings:
    def __init__(self):
        extensions = ['main']
        for extension in extensions:
            path = importlib.import_module(extension).__path__
            for loader, module_name, is_pkg in  pkgutil.walk_packages(path):
                import pdb;pdb.set_trace()


settings = GlobalSettings()