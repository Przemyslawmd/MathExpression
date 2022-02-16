
import sys

import pyqtgraph as pg
import numpy
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QMainWindow, QToolBar
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout
from PySide6.QtWidgets import QPushButton, QLineEdit, QTextEdit
from PySide6.QtCore import Slot
from PySide6.QtGui import QAction

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

        self.x_min = -360
        self.x_max = 360
        self.x_grid = True
        self.y_grid = True
        self.precision = 0.10

        self.create_gui()


    @Slot()
    def draw(self):
        self.create_new_graph(True)


    @Slot()
    def append(self):
        self.create_new_graph(False)


    @Slot()
    def clear_insert_area(self):
        self.insert_expression.clear()


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


    @Slot()
    def change_x_y_ratio(self, ratio):
        self.plot_widget.setXRange(self.x_min * ratio, self.x_max * ratio)


    def set_message(self, message):
        self.area_messages.clear()
        self.area_messages.setText(message)


    def create_new_graph(self, clear_plot_area):
        self.x_min, self.x_max = self.calculate_range(self.insert_x_min, self.insert_x_max)
        if self.x_min == 0 and self.x_max == 0:
            return

        if self.insert_y_min.text() or self.insert_y_max.text():
            if self.insert_y_min.text() and self.insert_y_max.text():
                y_min, y_max = self.calculate_range(self.insert_y_min, self.insert_y_max)
                if y_min == 0 and y_max == 0:
                    return
                self.plot_widget.setYRange(y_min, y_max, padding=0)
            else:
                self.set_message("Range error: only one value for Y range")
                return

        try:
            y = self.controller.calculate_values(self.insert_expression.text(), self.x_min, self.x_max, self.precision)
        except Exception as e:
            self.set_message(str(e))
            return

        if clear_plot_area is True:
            self.clear_plot_area()

        x = numpy.arange(self.x_min, self.x_max + self.precision, self.precision)
        line_width = float(self.list_pen_width.currentText())
        line_color = self.penColors[self.list_pen_color.currentText()]
        self.plot_lines.append(self.plot_widget.plot(x, y, pen=pg.mkPen(line_color, width=line_width), symbol='x',
                                                     symbolPen=None, symbolBrush=2.5, connect="finite"))

        self.area_messages.clear()


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
            self.set_message(f"Range error: {str(e)}")
            return 0, 0
        if min_value > max_value:
            self.set_message("Range error: minimum higher than maximum")
            return 0, 0
        return min_value, max_value


    @staticmethod
    def create_button(label, width, func):
        button = QPushButton(label)
        button.setMaximumWidth(width)
        button.setMinimumWidth(width)
        button.clicked.connect(func)
        return button


    def create_first_layout_buttons(self):
        layout = QHBoxLayout()

        layout.addWidget(self.create_button("Draw Graph", 140, lambda: self.draw()))
        layout.addSpacing(20)

        layout.addWidget(self.create_button("Append Graph", 140, lambda: self.append()))
        layout.addSpacing(20)

        self.insert_x_min.setMaximumWidth(50)
        self.insert_x_min.setText(str(self.x_min))
        layout.addWidget(QLabel("X Min"))
        layout.addWidget(self.insert_x_min)
        layout.addSpacing(10)

        self.insert_x_max.setMaximumWidth(50)
        self.insert_x_max.setText(str(self.x_max))
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
        self.list_pen_color.addItems(["Black", "Blue", "Green", "Light Blue", "Light Green", "Orange", "Red", "White",
                                      "Yellow"])
        self.list_pen_color.setCurrentIndex(4)
        layout.addWidget(QLabel("Line Color"))
        layout.addWidget(self.list_pen_color)
        layout.addStretch()
        return layout


    def create_second_layout_buttons(self):
        layout = QHBoxLayout()

        layout.addWidget(self.create_button("Clear Insert Area", 140, lambda: self.clear_insert_area()))
        layout.addSpacing(20)

        layout.addWidget(self.create_button("Clear Plot Area", 140, lambda: self.clear_plot_area()))
        layout.addSpacing(20)

        self.insert_y_min.setMaximumWidth(50)
        self.insert_y_min.setText("")
        layout.addWidget(QLabel("Y Min"))
        layout.addWidget(self.insert_y_min)
        layout.addSpacing(10)

        self.insert_y_max.setMaximumWidth(50)
        self.insert_y_max.setText("")
        layout.addWidget(QLabel("Y Max"))
        layout.addWidget(self.insert_y_max)
        layout.addSpacing(20)

        layout.addWidget(QLabel("X Y ratio"))
        layout.addSpacing(15)
        layout.addWidget(self.create_button("8/1", 40, lambda: self.change_x_y_ratio(0.125)))
        layout.addSpacing(20)
        layout.addWidget(self.create_button("4/1", 40, lambda: self.change_x_y_ratio(0.25)))
        layout.addSpacing(20)
        layout.addWidget(self.create_button("2/1", 40, lambda: self.change_x_y_ratio(0.5)))
        layout.addSpacing(20)
        layout.addWidget(self.create_button("1/1", 40, lambda: self.change_x_y_ratio(1)))
        layout.addSpacing(20)
        layout.addWidget(self.create_button("1/2", 40, lambda: self.change_x_y_ratio(2)))
        layout.addSpacing(20)
        layout.addWidget(self.create_button("1/4", 40, lambda: self.change_x_y_ratio(4)))
        layout.addSpacing(20)
        layout.addWidget(self.create_button("1/8", 40, lambda: self.change_x_y_ratio(8)))
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


    def apply_settings(self, x_grid, y_grid, precision):
        self.x_grid = x_grid
        self.y_grid = y_grid
        self.precision = precision
        self.plot_widget.showGrid(x=self.x_grid, y=self.y_grid)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MathExpression()
    widget.resize(1200, 800)
    widget.show()
    sys.exit(app.exec())


