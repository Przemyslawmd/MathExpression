
import sys

from PySide2 import QtCore

from Controller import Controller

from PySide2.QtWidgets import (QApplication, QWidget, QLabel, QListWidget, QComboBox)
from PySide2.QtWidgets import (QVBoxLayout, QHBoxLayout, QGridLayout)
from PySide2.QtWidgets import (QPushButton, QLineEdit, QTextEdit)
from PySide2.QtCore import Slot

from pyqtgraph import PlotWidget, plot, mkPen
import pyqtgraph as pg

class MathExpression(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        self.controller = Controller()
        self.plot_widget = pg.PlotWidget()
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
            self.area_messages.append(str(value))
        return

    @Slot()
    def append(self):
        try:
            values = self.controller.calculate_values(self.line_insert.text())
        except Exception as e:
            self.area_messages.append(str(e))
            return

        for value in values:
            self.area_messages.append(str(value))
        return


    @Slot()
    def clear_insert_area(self):
        self.area_messages.append("Clear Insert Area")


    @Slot()
    def clear_plot_area(self):
        self.area_messages.append("Clear Plot Area")


    @Slot()
    def clear(self):
        self.line_insert.clear()


    def create_button(self, label, func):
        button = QPushButton(label)
        button.setMaximumWidth(140)
        button.setMinimumWidth(140)
        button.clicked.connect(func)
        return button


    def create_gui(self):

        layout_main = QVBoxLayout()

        layout_main.addSpacing(20)
        layout_main.addWidget(self.line_insert)
        layout_main.addSpacing(10)

        layout_buttons_1 = QHBoxLayout()

        button_draw = self.create_button("Draw Graph", lambda: self.draw())
        layout_buttons_1.addWidget(button_draw)
        layout_buttons_1.addSpacing(20)

        button_append = self.create_button("Append Graph", lambda: self.append())
        layout_buttons_1.addWidget(button_append)
        layout_buttons_1.addSpacing(20)

        label_x_min = QLabel("X Min")
        label_x_min.setMaximumWidth(35)
        edit_x_min = QLineEdit()
        edit_x_min.setMaximumWidth(50)
        layout_buttons_1.addWidget(label_x_min)
        layout_buttons_1.addWidget(edit_x_min)
        layout_buttons_1.addSpacing(10)

        label_x_max = QLabel("X Max")
        label_x_max.setMaximumWidth(40)
        edit_x_max = QLineEdit()
        edit_x_max.setMaximumWidth(50)
        layout_buttons_1.addWidget(label_x_max)
        layout_buttons_1.addWidget(edit_x_max)
        layout_buttons_1.addSpacing(20)

        label_line_width = QLabel("Line Width")
        label_line_width.setMaximumWidth(70)
        edit_line_width = QLineEdit()
        edit_line_width.setMaximumWidth(50)
        layout_buttons_1.addWidget(label_line_width)
        layout_buttons_1.addWidget(edit_line_width)
        layout_buttons_1.addSpacing(20)

        label_line_color = QLabel("Line Color")
        label_line_color.setMaximumWidth(70)
        list_color = QComboBox()
        list_color.setMaximumWidth(80)
        list_color.addItem("Blue")
        list_color.addItem("Green")
        list_color.addItem("Orange")
        list_color.addItem("Red")
        list_color.addItem("White")
        list_color.addItem("Yellow")

        layout_buttons_1.addWidget(label_line_color)
        layout_buttons_1.addWidget(list_color)
        layout_buttons_1.addStretch()

        layout_main.addLayout(layout_buttons_1)
        layout_main.addSpacing(20)

        layout_buttons_2 = QHBoxLayout()

        button_clear_edit = self.create_button("Clear Insert Area", lambda: self.clear_insert_area())
        layout_buttons_2.addWidget(button_clear_edit)
        layout_buttons_2.addSpacing(20)

        button_clear_plot = self.create_button("Clear Plot Area", lambda: self.clear_plot_area())
        layout_buttons_2.addWidget(button_clear_plot)
        layout_buttons_2.addSpacing(20)
        layout_buttons_2.addStretch()

        layout_main.addLayout(layout_buttons_2)
        layout_main.addSpacing(20)

        x = range(0, 10)

        self.plot_widget.setXRange(0, 10)
        self.plot_widget.setYRange(0, 10)

        y = [1, 2, 3, 4, 50, 6, 7, 8, 9, 10]

        mkPen('y', width=30, style=QtCore.Qt.DashLine)
        line = self.plot_widget.plot(x, y, pen=pg.mkPen(width=2), symbol='x', symbolPen=None, symbolBrush=2.5, name='red')

        self.plot_widget.showGrid(x=True, y=True)
        layout_main.addWidget(self.plot_widget)
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

