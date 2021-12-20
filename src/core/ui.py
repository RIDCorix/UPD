from typing import Any, Hashable, Optional

import datetime

from contextlib import contextmanager
from PySide6 import QtCore

from PySide6.QtGui import QPalette
from PySide6.QtCore import QPropertyAnimation
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QColorDialog

class RWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def slide(self, att: str, from_value: Any, to_value: Any, duration: int=500, callback: Optional[str]=None):
        self.anim = QPropertyAnimation(self, att.encode())
        self.anim.setStartValue(from_value)
        self.anim.setEndValue(to_value)
        self.anim.valueChanged.connect(self._update)
        self.anim.setDuration(duration)

        if callback:
            self.anim.finished.connect(getattr(self, callback))

        self.anim.start(QtCore.QAbstractAnimation.DeleteWhenStopped)

    def _update(self):
        print(self.anim.currentValue())


class ConsoleBlock:
    def __init__(self, root=None, parent=None, text='', auto_update=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if root is None:
            self.root = self
        else:
            self.root = root

        self._text = text
        self.parent = parent
        self.blocks = []

        self.auto_update = False
        self._index = 0
        self._title = ''
        self._total = 1

    def finish(self):
        self.console.finish_block(self.block_id)

    def line(self, text:str):
        self.out(str(text))
        self.root.update()

    def progress(self, title:str, done: int, total: int):
        self._title = title
        self._total = total
        self.replace(f'Loading... ({done} of {total}) | {done*100/total} %')

    def done(self):
        self.replace(f'{self._title} ({self._total} of {self._total}) | <font color="green">Done</font>', flush=True)


    def out(self, text: str):
        self.blocks.append(ConsoleBlock(self.root, self, str(text)))
        self.root.update()

    def replace(self, text: str, **kwargs):
        self._text = text
        self.root.update(**kwargs)

    @contextmanager
    def block(self, temp=False):
        block = ConsoleBlock(self.root, self)
        self.blocks.append(block)
        yield block
        if temp:
            del block


    def get_text(self, depth=0, anim=True, flush=False):
        if flush:
            self._index = len(self._text)

        if self._text:
            if anim:
                _text = self._text[:int(self._index)]
            else:
                _text = self._text

            self._index += (len(self._text) - self._index) / 4 + 1

            if self.blocks:
                text = '| . ' * depth + 'o ' + _text + '<br>'
            else:
                text = '| . ' * depth + _text + '<br>'
        else:
            text = ''
            depth -= 1

        for block in self.blocks:
            text += block.get_text(depth+1, anim=anim, flush=flush)
        return text

class Console(QLabel, ConsoleBlock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ConsoleBlock.__init__(self)

    def update(self, *args, **kwargs):
        self.setText(self.get_text(**kwargs))
        super().update()


class ColorPicker(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = QVBoxLayout(self)
        button = QPushButton("Select color")
        button.clicked.connect(self.on_clicked)
        self.label = QLabel()
        self.label.setAutoFillBackground(True)
        self.label.setFixedSize(100, 100)

        layout.addWidget(button)
        layout.addWidget(self.label)

    def on_clicked(self):
        color = QColorDialog.getColor()
        if color.isValid():
            palette = self.label.palette()
            palette.setColor(QPalette.Background, color)
            self.label.setPalette(palette)
