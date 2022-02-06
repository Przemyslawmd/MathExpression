
import sys

import numpy
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QComboBox, QMainWindow, QToolBar)
from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout)
from PySide6.QtWidgets import (QPushButton, QLineEdit, QTextEdit)
from PySide6.QtCore import Slot
from PySide6.QtGui import QAction
import pyqtgraph as pg

from Controller import Controller
from WindowAbout import WindowAbout
from WindowSettings import WindowSettings


class MathExpression(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        self.controller = Controller()
        self.plot_widget = pg.PlotWidget()

        self.insert_expression = QLineEdit()
        self.insert_x_min = QLineEdit()
        self.insert_x_max = QLineEdit()
        self.insert_y_min = QLineEdit()
        self.insert_y_max = QLineEdit()

        self.list_pen_width = QComboBox()
        self.list_pen_color = QComboBox()
        self.area_messages = QTextEdit()

        self.plot_lines = []
        self.penColors = {
            "Black": [0, 0, 0], "Blue": [0, 0, 255], "Green": [0, 128, 0], "Light Blue": [0, 191, 255],
            "Light Green": [0, 255, 128], "Orange": [255, 140, 0], "Red": [255, 0, 0],
            "Yellow": [255, 255, 0], "White": [255, 255, 255]
        }

        self.x_grid = True
        self.y_grid = True
        self.x_precision = 1.00

        self.create_gui()


    @Slot()
    def draw(self):
        self.create_new_graph(True)


    @Slot()
    def append(self):
        self.create_new_graph(False)


    @Slot()
    def clear_insert_area(self):
        self.line_insert.clear()


    @Slot()
    def clear_plot_area(self):
        for line in self.plot_lines:
            self.plot_widget.removeItem(line)
        self.plot_lines.clear()


    @Slot()
    def widget_settings(self):
        WindowSettings(self)


    @Slot()
    def window_about(self):
        WindowAbout()


    def create_new_graph(self, clear_plot_area):
        x_min, x_max = self.calculate_range(self.insert_x_min, self.insert_x_max)
        if x_min == 0 and x_max == 0:
            return

        if self.insert_y_min.text() != "No" or self.insert_y_max.text() != "No":
            y_min, y_max = self.calculate_range(self.insert_y_min, self.insert_y_max)
            if y_min == 0 and y_max == 0:
                return
            self.plot_widget.setYRange(y_min, y_max, padding=0)

        try:
            y = self.controller.calculate_values(self.insert_expression.text(), x_min, x_max, self.x_precision)
        except Exception as e:
            self.area_messages.append(str(e))
            return

        if clear_plot_area is True:
            self.clear_plot_area()

        x = numpy.arange(x_min, x_max + self.x_precision, self.x_precision)
        line_width = float(self.list_pen_width.currentText())
        line_color = self.penColors[self.list_pen_color.currentText()]
        self.plot_lines.append(self.plot_widget.plot(x, y, pen=pg.mkPen(line_color, width=line_width), symbol='x',
                                                     symbolPen=None, symbolBrush=2.5, name='red', connect="finite"))


    def calculate_range(self, insert_min, insert_max):
        min_str = insert_min.text().lstrip()
        max_str = insert_max.text().lstrip()

        min_negative = False
        max_negative = False
        if min_str[0] == '-':
            min_negative = True
            min_str = min_str[1:]
        if max_str[0] == '-':
            max_negative = True
            max_str = max_str[1:]

        try:
            min_value = float(min_str) if min_negative is False else float(min_str) * -1
            max_value = float(max_str) if max_negative is False else float(max_str) * -1
        except Exception as e:
            self.area_messages.append("Error: Parse range values")
            self.area_messages.append(str(e))
            return 0, 0
        if min_value > max_value:
            self.area_messages.append("Error: Range minimum higher than maximum")
            return 0, 0
        return min_value, max_value


    def create_button(self, label, func):
        button = QPushButton(label)
        button.setMaximumWidth(140)
        button.setMinimumWidth(140)
        button.clicked.connect(func)
        return button


    def create_first_layout_buttons(self):
        layout = QHBoxLayout()

        button_draw = self.create_button("Draw Graph", lambda: self.draw())
        layout.addWidget(button_draw)
        layout.addSpacing(20)

        button_append = self.create_button("Append Graph", lambda: self.append())
        layout.addWidget(button_append)
        layout.addSpacing(20)

        self.insert_x_min.setMaximumWidth(50)
        self.insert_x_min.setText("-2")
        layout.addWidget(QLabel("X Min"))
        layout.addWidget(self.insert_x_min)
        layout.addSpacing(10)

        self.insert_x_max.setMaximumWidth(50)
        self.insert_x_max.setText("2")
        layout.addWidget(QLabel("X Max"))
        layout.addWidget(self.insert_x_max)
        layout.addSpacing(20)

        self.list_pen_width.setMaximumWidth(50)
        for i in [0.1, 0.2, 0.3, 0.4, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 7, 8, 9, 10]:
            self.list_pen_width.addItem(str(i))
        self.list_pen_width.setCurrentIndex(4)
        layout.addWidget(QLabel("Line Width"))
        layout.addWidget(self.list_pen_width)
        layout.addSpacing(20)

        self.list_pen_color.setMaximumWidth(100)
        for color in ["Black", "Blue", "Green", "Light Blue", "Light Green", "Orange", "Red", "White", "Yellow"]:
            self.list_pen_color.addItem(color)
        self.list_pen_color.setCurrentIndex(4)
        layout.addWidget(QLabel("Line Color"))
        layout.addWidget(self.list_pen_color)
        layout.addStretch()
        return layout


    def create_second_layout_buttons(self):
        layout = QHBoxLayout()

        button_clear_edit = self.create_button("Clear Insert Area", lambda: self.clear_insert_area())
        layout.addWidget(button_clear_edit)
        layout.addSpacing(20)

        button_clear_plot = self.create_button("Clear Plot Area", lambda: self.clear_plot_area())
        layout.addWidget(button_clear_plot)
        layout.addSpacing(20)

        self.insert_y_min.setMaximumWidth(50)
        self.insert_y_min.setText("No")
        layout.addWidget(QLabel("Y Min"))
        layout.addWidget(self.insert_y_min)
        layout.addSpacing(10)

        self.insert_y_max.setMaximumWidth(50)
        self.insert_y_max.setText("No")
        layout.addWidget(QLabel("Y Max"))
        layout.addWidget(self.insert_y_max)
        layout.addSpacing(20)
        return layout


    def create_gui(self):
        tool_bar = QToolBar()
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(lambda: self.widget_settings())
        tool_bar.addAction(settings_action)
        about_action = QAction("About", self)
        about_action.triggered.connect(lambda: self.window_about())
        tool_bar.addAction(about_action)
        self.addToolBar(tool_bar)

        layout_main = QVBoxLayout()
        layout_main.addSpacing(20)
        layout_main.addWidget(self.insert_expression)
        layout_main.addSpacing(10)

        layout_buttons_first = self.create_first_layout_buttons()
        layout_main.addLayout(layout_buttons_first)
        layout_main.addSpacing(20)

        layout_buttons_second = self.create_second_layout_buttons()
        layout_buttons_second.addStretch()
        layout_main.addLayout(layout_buttons_second)
        layout_main.addSpacing(20)

        self.plot_widget.showGrid(x=self.x_grid, y=self.y_grid)
        layout_main.addWidget(self.plot_widget)
        layout_main.addSpacing(20)

        layout_main.addWidget(self.area_messages)
        self.area_messages.setMaximumHeight(100)
        layout_main.addSpacing(20)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_widget.setLayout(layout_main)
        main_widget.setContentsMargins(20, 0, 20, 0)


    def apply_settings(self, x_grid, y_grid, x_precision):
        self.x_grid = x_grid
        self.y_grid = y_grid
        self.x_precision = x_precision
        self.plot_widget.showGrid(x=self.x_grid, y=self.y_grid)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MathExpression()
    widget.resize(1200, 800)
    widget.show()
    sys.exit(app.exec())


