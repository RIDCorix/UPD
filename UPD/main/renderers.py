from PySide6.QtCore import QPoint, QRect
from PySide6.QtGui import QBrush, QColor, QFont, QPainter, QPalette, QPen, QPixmap, QRadialGradient
from .tool import tool
from upd.renderers import RWidgetRenderer
@tool.renderer
class RFloatPanelRenderer(RWidgetRenderer):
    def __init__(self):
        self.name = 'Float Panel'

    def render(self, widget):
        painter = QPainter()
        painter.begin(widget)
        painter.setPen(QPen(QColor(255, 255, 255), 2))

        painter.drawRect(widget.rect())
        painter.setPen(QPen(QColor(255, 255, 255), 0))
        painter.setBrush(QBrush(QColor(0, 0, 0, 100)))
        rect = widget.rect()
        size = rect.bottomRight()
        short = min(rect.width(), rect.height())
        widget.shrink = QPoint(short, short) / 20
        rect = QRect(widget.shrink, size-widget.shrink)
        painter.drawRect(rect)
        painter.end()
