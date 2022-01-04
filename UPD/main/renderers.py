from PySide6.QtCore import QPoint, QPointF, QRect, QSize
from PySide6.QtGui import QBrush, QColor, QFont, QPainter, QPalette, QPen, QPixmap, QRadialGradient
from .tool import tool
from upd.renderers import RWidgetRenderer
from upd.ui import Renderable
from upd.conf import settings
from upd.options import ColorOption


@tool.renderer
class RFloatPanelRenderer(RWidgetRenderer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_options(
            panel_color=ColorOption('Panel Color', QColor(0, 0, 0, 100)),
            text_color=ColorOption('Text Color', QColor(255, 255, 255)),
            border_color=ColorOption('Border Color', QColor(255, 255, 255)),
            background_color=ColorOption('Panel Color', QColor(0, 0, 0, 100)),
        )
        self.name = 'Float Panel'

    def render_button(self, widget, event):
        super(Renderable, widget).paintEvent(event)

    def render_main_panel(self, widget, event):
        (
            background_color,
            border_color,
            panel_color,
            text_color,
        ) = self.get_options('background_color', 'border_color', 'panel_color', 'text_color')

        painter = QPainter()
        painter.begin(widget)
        painter.setPen(QPen(border_color, 2))

        painter.drawRect(widget.rect())
        painter.setPen(QPen(border_color, 0))
        painter.setBrush(QBrush(panel_color))
        rect = widget.rect()
        size = rect.bottomRight()
        short = min(rect.width(), rect.height())
        widget.shrink = QPoint(short, short) / 20
        rect = QRect(widget.shrink, size-widget.shrink)
        painter.drawRect(rect)
        painter.end()

    def render_line_edit(self, widget ,event):
        (
            background_color,
            border_color,
            panel_color,
            text_color,
        ) = self.get_options('background_color', 'border_color', 'panel_color', 'text_color')

        painter = QPainter()
        painter.begin(widget)
        start = QPointF(0, widget.size().height()/2)
        gradient = QRadialGradient(start, 50)

        gradient.setColorAt(0, panel_color)
        color = QColor(panel_color)
        color.a = 0
        gradient.setColorAt(widget.focus_rate, color)

        painter.setBrush(QBrush(gradient))
        painter.drawRect(widget.rect())
        painter.end()
        super(Renderable, widget).paintEvent(event)

    def render_text_edit(self, widget ,event):
        (
            background_color,
            border_color,
            panel_color,
            text_color,
        ) = self.get_options('background_color', 'border_color', 'panel_color', 'text_color')

        widget.text_edit.setStyleSheet(f'QWidget{{color: rgba{text_color.toTuple()};}}')
        painter = QPainter()
        painter.begin(widget)
        start = QPointF(0, widget.size().height()/2)
        gradient = QRadialGradient(start, 200)
        gradient.setCenter(0, 0)
        gradient.setColorAt(0, QColor(panel_color))
        color = QColor(panel_color.value())
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

    def render_loading_screen(self, widget, event):
        (
            background_color,
            border_color,
            panel_color,
            text_color,
        ) = self.get_options('background_color', 'border_color', 'panel_color', 'text_color')

        self.render_main_panel(widget, event)
        widget.console.update()

        center = widget.rect().center()
        width = widget.rect().width()
        height = widget.rect().height()

        widget.label.move(center - QPoint(0, 50+height * (1-widget.drop_rate) / 20) - widget.label.rect().center())
        widget.console_area.move(center + QPoint(0, 150+height * (1-widget.drop_rate) / 20) - widget.console_area.rect().center())

        if widget.drop_rate < 1:
            widget.label.graphicsEffect().setOpacity(widget.drop_rate)
            widget.console.graphicsEffect().setOpacity(widget.drop_rate)

        painter = QPainter()
        painter.begin(widget)
        painter.setPen(QPen(border_color, 2))
        painter.drawLine(center - QPoint(width * widget.drop_rate / 5, 0), center + QPoint(width * widget.drop_rate / 5, 0))

        painter.end()

    def render_graph_node(self, widget, event):
        (
            background_color,
            border_color,
            panel_color,
            text_color,
        ) = self.get_options('background_color', 'border_color', 'panel_color', 'text_color')

        widget.connector.setStyleSheet(f'background-color: rgba(255, 255, 255, {widget.connector_rate});color: rgba(0, 0, 0, {widget.connector_rate});')
        if not widget.removed:
            widget.parent().update()
            self.render_main_panel(widget, event)
            widget.header.setFixedWidth(max(widget.size().width(), 150))
            widget.header.slide('size', to_value=QSize(widget.size().width(), 50))
            widget.connector.move(widget.pos()+widget.rect().center()-widget.connector.rect().center() + QPoint(0, -50*widget.connector_rate))

    def render_graph(self, widget, event):
        self.render_main_panel(widget, event)
        painter = QPainter()
        painter.begin(widget)
        painter.setPen(QColor(255, 255, 255))
        for item in widget.connection_data:
            if item['id'] not in widget.connections:
                from_node = widget.nodes[item['from_node']]
                to_node = widget.nodes[item['to_node']]

            from_point = from_node.pos() + from_node.rect().center()
            to_point = to_node.pos() + to_node.rect().center()
            painter.drawLine(from_point, to_point)

        painter.end()


@tool.renderer
class PlainRenderer(RWidgetRenderer):
    def __init__(self):
        self.name = 'no style'

    def render(self, widget, event):
        return super(Renderable, widget).paintEvent(event)

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
