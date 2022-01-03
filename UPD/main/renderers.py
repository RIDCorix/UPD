from PySide6.QtCore import QPoint, QPointF, QRect
from PySide6.QtGui import QBrush, QColor, QFont, QPainter, QPalette, QPen, QPixmap, QRadialGradient
from .tool import tool
from upd.renderers import RWidgetRenderer
from upd.ui import Renderable
from upd.conf import settings
@tool.renderer
class RFloatPanelRenderer(RWidgetRenderer):
    def __init__(self):
        self.name = 'Float Panel'

    def render(self, widget, event):
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

    def render_button(self, widget, event):
        super(Renderable, widget).paintEvent(event)

    def render_main_panel(self, widget, event):
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

    def render_line_edit(self, widget ,event):

        painter = QPainter()
        painter.begin(widget)
        start = QPointF(0, widget.size().height()/2)
        gradient = QRadialGradient(start, 50)

        gradient.setColorAt(0, QColor(0, 0, 0))
        color = QColor(255, 255, 255, 100)
        color.a = 0
        gradient.setColorAt(widget.focus_rate, color)

        painter.setBrush(QBrush(gradient))
        painter.drawRect(widget.rect())
        painter.end()
        super(Renderable, widget).paintEvent(event)

    def render_item(self, widget, event):
        widget.label.resize(widget.size())

        painter = QPainter()
        painter.begin(widget)
        painter.setPen(QPen(settings.BORDER_COLOR, 5))
        for x in range(2):
            x *= widget.width()
            for y in range(2):
                y *= widget.height()
                pos = (x, y)
                p_pos = QPoint(*pos)
                cent = widget.rect().center()
                cent.setX(x)
                cent = p_pos + (cent-p_pos)*widget.focus_rate/2
                painter.drawLine(p_pos, cent)
                cent = widget.rect().center()
                cent.setY(y)
                cent = p_pos + (cent-p_pos)*widget.focus_rate/2
                painter.drawLine(p_pos, cent)

        shrink = QPoint(20, 20) * widget.focus_rate
        color = settings.PANEL_COLOR
        color.setAlpha(min(color.alpha() * (0.5+widget.focus_rate/2), 255))
        painter.setBrush(color)
        painter.drawRect(QRect(widget.rect().topLeft() + shrink, widget.rect().bottomRight() - shrink))

        painter.end()


@tool.renderer
class PlainRenderer(RWidgetRenderer):
    def __init__(self):
        self.name = 'no style'

    def render(self, widget, event):
        return super(Renderable, widget).paintEvent(event)
