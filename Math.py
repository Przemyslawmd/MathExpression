

import sys

from Controller import Controller

from PySide2.QtWidgets import (QApplication, QWidget, QLabel, QListWidget, QComboBox)
from PySide2.QtWidgets import (QVBoxLayout, QHBoxLayout, QGridLayout)
from PySide2.QtWidgets import (QPushButton, QLineEdit, QTextEdit)
from PySide2.QtCore import Slot

import pyqtgraph as pg


class MathExpression(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        self.controller = Controller()
        self.plot_widget = pg.PlotWidget()
        self.line_insert = QLineEdit()
        self.insert_x_min = QLineEdit()
        self.insert_x_max = QLineEdit()
        self.edit_line_width = QComboBox()
        self.list_color = QComboBox()
        self.area_messages = QTextEdit()
        self.plot_lines = []

        self.penColors = {"Black": [0, 0, 0], "Blue": [0, 0, 255], "Green": [0, 128, 0], "Orange": [255, 140, 0],
                          "Red": [255, 0, 0], "Yellow": [255, 255, 0], "White": [255, 255, 255]}

        self.create_gui()


    @Slot()
    def draw(self):
        try:
            x_min = int(self.insert_x_min.text())
            x_max = int(self.insert_x_max.text())
        except Exception:
            self.area_messages.append("X minimum or maximum value error")
            return

        try:
            y = self.controller.calculate_values(self.line_insert.text(), x_min, x_max)
        except Exception as e:
            self.area_messages.append(str(e))
            return

        x = range(x_min, x_max + 1)
        line_width = float(self.edit_line_width.currentText())
        line_color = self.penColors[self.list_color.currentText()]
        self.plot_lines.append(self.plot_widget.plot(x, y, pen=pg.mkPen(line_color, width=line_width), symbol='x',
                                                     symbolPen=None, symbolBrush=2.5, name='red'))


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
        self.line_insert.clear()


    @Slot()
    def clear_plot_area(self):
        for line in self.plot_lines:
            self.plot_widget.removeItem(line)
        self.plot_lines.clear()


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
        self.insert_x_min.setMaximumWidth(50)
        self.insert_x_min.setText("0")
        layout_buttons_1.addWidget(label_x_min)
        layout_buttons_1.addWidget(self.insert_x_min)
        layout_buttons_1.addSpacing(10)

        label_x_max = QLabel("X Max")
        label_x_max.setMaximumWidth(40)
        self.insert_x_max.setMaximumWidth(50)
        self.insert_x_max.setText("3600")
        layout_buttons_1.addWidget(label_x_max)
        layout_buttons_1.addWidget(self.insert_x_max)
        layout_buttons_1.addSpacing(20)

        label_line_width = QLabel("Line Width")
        label_line_width.setMaximumWidth(70)
        self.edit_line_width.setMaximumWidth(50)
        line_sizes = [0.1, 0.2, 0.3, 0.4, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 7, 8, 9, 10]
        for i in line_sizes:
            self.edit_line_width.addItem(str(i))
        layout_buttons_1.addWidget(label_line_width)
        layout_buttons_1.addWidget(self.edit_line_width)
        layout_buttons_1.addSpacing(20)

        label_line_color = QLabel("Line Color")
        label_line_color.setMaximumWidth(70)
        self.list_color.setMaximumWidth(80)
        line_colors = ["Black", "Blue", "Green", "Orange", "Red", "White", "Yellow"]
        for color in line_colors:
            self.list_color.addItem(color)

        layout_buttons_1.addWidget(label_line_color)
        layout_buttons_1.addWidget(self.list_color)
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

        self.plot_widget.showGrid(x=True, y=True)

        layout_main.addWidget(self.plot_widget)
        layout_main.addSpacing(20)

        layout_main.addWidget(self.area_messages)
        layout_main.addSpacing(20)

        self.setLayout(layout_main)
        self.setContentsMargins(20, 0, 20, 0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MathExpression()
    widget.resize(1200, 800)
    widget.show()
    sys.exit(app.exec_())


