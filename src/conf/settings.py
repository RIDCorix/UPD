from typing import List, Dict

from core.options import Optionable, Option

class Settings():
    pass


class SettingsCategory(Optionable):
    def __getattr__(self, attr):
        return self.options[attr].value

class Configuration:
    def __init__(self, *args, **kwargs):
        self.categories = {}

    def add_category(self, name: str, **settings: Dict[str, Option]):
        self.categories[name] = SettingsCategory(**settings)

    def get(self, name):
        return 

    def __getattr__(self, attr):
        try:
            return self.categories[attr]
        except:
            for name, category in self.categories.items():
                return category.options[attr].value

    def to_dict(self):
        settings_map = {}
        for name, category in self.categories.items():
            for setting_name, option in category.options.items():
                settings_map[setting_name] = option.to_str()
        return settings_map