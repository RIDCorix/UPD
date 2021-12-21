from PySide6.QtGui import QColor

from upd.options import ColorOption, FontOption
from upd.conf import Configuration
from . import tasks
settings = Configuration()

settings.add_category('preference',
    TEXT_COLOR=ColorOption('Text Color', QColor(255, 255, 255)),
    THEME_COLOR=ColorOption('Theme Color', QColor(255, 255, 255)),
    PANEL_COLOR=ColorOption('Panel Color', QColor(0, 0, 0, 100)),
    BORDER_COLOR=ColorOption('Border Color', QColor(255, 255, 255)),
    FONT_MONO=FontOption('Font (mono)', 'Share Tech Mono'),
    FONT_NORMAL=FontOption('Font (normal)', 'caveat'),
    FONT_HANDWRITING=FontOption('Font (handwriting)', 'caveat'),
)
