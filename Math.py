
import sys

from Controller import Controller

from PySide2.QtWidgets import (QApplication, QWidget)
from PySide2.QtWidgets import (QVBoxLayout, QHBoxLayout, QGridLayout)
from PySide2.QtWidgets import (QPushButton, QLineEdit, QTextEdit)
from PySide2.QtCore import Slot

from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

class MathExpression(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        self.controller = Controller()
        self.plot = pg.PlotWidget()
        self.line_insert = QLineEdit()
        self.area_messages = QTextEdit()
        self.create_gui()


    @Slot()
    def draw(self):
        try:
            values = self.controller.calculate_values(self.line_insert.text())
        except Exception as e:
            self.area_messages.append(str(e))
            return

        for value in values:
            self.area_messages.append(str(value[0]))
        return


    @Slot()
    def clear(self):
        self.line_insert.clear()


    def add_button(self, layout, func, width, label, row, column, column_span=1):
        button = QPushButton(label)
        button.setMaximumWidth(width)
        button.setMinimumWidth(width)
        button.clicked.connect(func)
        layout.addWidget(button, row, column, 1, column_span)


    def create_gui(self):

        layout_insert = QHBoxLayout()
        layout_insert.addWidget(self.line_insert)

        button_draw = QPushButton("Draw")
        button_draw.setMaximumWidth(220)
        button_draw.clicked.connect(lambda: self.draw())
        layout_insert.addWidget(button_draw)

        layout_main = QVBoxLayout()
        layout_main.addSpacing(20)
        layout_main.addLayout(layout_insert, 68)
        layout_main.addSpacing(20)

        self.plot.showGrid(x=True, y=True)
        layout_main.addWidget(self.plot)
        layout_main.addSpacing(20)

        layout_main.addWidget(self.area_messages)
        layout_main.addSpacing(20)

        self.setLayout(layout_main)
        self.setContentsMargins(20, 0, 20, 0)

        return


if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = MathExpression()
    widget.resize(1200, 800)
    widget.show()

    sys.exit(app.exec_())

