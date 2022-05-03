
import sys

from numpy import arange

from PySide6.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QMainWindow, QToolBar
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout
from PySide6.QtWidgets import QPushButton, QLineEdit, QTextEdit
from PySide6.QtCore import Slot
from PySide6.QtGui import Qt, QAction
from pyqtgraph import PlotWidget, mkPen

from Controller import Controller
from WindowAbout import WindowAbout
from WindowSettings import WindowSettings


class MathExpression(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        self.controller = Controller()
        self.plot_widget = PlotWidget()

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

        self.ratio_button_active = None
        self.ratio_buttons = None

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
    def change_x_y_ratio(self, ratio, button_index):
        self.plot_widget.setXRange(self.x_min * ratio, self.x_max * ratio)
        self.ratio_button_active.setStyleSheet("")
        self.ratio_button_active = self.ratio_buttons[button_index]
        self.ratio_button_active.setStyleSheet("background-color : #b3b3b3")

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

        x = arange(self.x_min, self.x_max + self.precision, self.precision)
        line_width = float(self.list_pen_width.currentText())
        line_color = self.penColors[self.list_pen_color.currentText()]
        self.plot_lines.append(self.plot_widget.plot(x, y, pen=mkPen(line_color, width=line_width), symbol='x',
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


    @staticmethod
    def create_widget_with_label(new_widget, width, text, text_width, default_value=""):
        new_widget.setMinimumWidth(width)
        new_widget.setMaximumWidth(width)
        if isinstance(new_widget, QLineEdit):
            new_widget.setText(default_value)
            new_widget.setAlignment(Qt.AlignCenter)
        label = QLabel(text)
        label.setFixedSize(text_width, 10)
        label.setMargin(0)
        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.setSpacing(5)
        layout.addWidget(new_widget)
        layout.addSpacing(10)
        return layout


    def create_first_grid_row(self, layout):
        layout.addWidget(self.create_button("Draw Graph", 140, lambda: self.draw()), 0, 0)
        layout.addWidget(self.create_button("Append Graph", 140, lambda: self.append()), 0, 1)
        layout.setSpacing(15)

        widget_with_label = self.create_widget_with_label(self.insert_x_min, 40, "X Min", 40, str(self.x_min))
        layout.addLayout(widget_with_label, 0, 3)

        widget_with_label = self.create_widget_with_label(self.insert_x_max, 40, "X Max", 40, str(self.x_max))
        layout.addLayout(widget_with_label, 0, 4)

        [self.list_pen_width.addItem(str(x))
         for x in [0.1, 0.2, 0.3, 0.4, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 7, 8, 9, 10]]
        self.list_pen_width.setCurrentIndex(4)
        widget_with_label = self.create_widget_with_label(self.list_pen_width, 100, "Line Width", 65)
        layout.addLayout(widget_with_label, 0, 6)

        layout_hor = QHBoxLayout()
        layout_hor.setSpacing(8)
        label = QLabel("X : Y Ratio")
        label.setFixedSize(60, 10)
        layout_hor.addWidget(label)

        self.ratio_buttons = [self.create_button("8/1", 50, lambda: self.change_x_y_ratio(0.125, 0)),
                              self.create_button("4/1", 50, lambda: self.change_x_y_ratio(0.25, 1)),
                              self.create_button("2/1", 50, lambda: self.change_x_y_ratio(0.5, 2)),
                              self.create_button("1/1", 50, lambda: self.change_x_y_ratio(1, 3)),
                              self.create_button("1/2", 50, lambda: self.change_x_y_ratio(2, 4)),
                              self.create_button("1/4", 50, lambda: self.change_x_y_ratio(4, 5)),
                              self.create_button("1/8", 50, lambda: self.change_x_y_ratio(8, 6))]
        [layout_hor.addWidget(button) for button in self.ratio_buttons]
        self.ratio_button_active = self.ratio_buttons[3]
        self.ratio_button_active.setStyleSheet("background-color : #b3b3b3")
        layout.addLayout(layout_hor, 0, 7)


    def create_second_grid_row(self, layout):
        layout.addWidget(self.create_button("Clear Insert Area", 140, lambda: self.clear_insert_area()), 1, 0)
        layout.addWidget(self.create_button("Clear Plot Area", 140, lambda: self.clear_plot_area()), 1, 1)

        widget_with_label = self.create_widget_with_label(self.insert_y_min, 40, "Y Min", 40)
        layout.addLayout(widget_with_label, 1, 3)

        widget_with_label = self.create_widget_with_label(self.insert_y_max, 40, "Y Max", 40)
        layout.addLayout(widget_with_label, 1, 4)

        self.list_pen_color.addItems(["Black", "Blue", "Green", "Light Blue", "Light Green", "Orange", "Red", "White",
                                      "Yellow"])
        self.list_pen_color.setCurrentIndex(4)
        widget_with_label = self.create_widget_with_label(self.list_pen_color, 100, "Line Color", 65)
        layout.addLayout(widget_with_label, 1, 6)


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

        layout_grid = QGridLayout()
        self.create_first_grid_row(layout_grid)
        self.create_second_grid_row(layout_grid)
        layout_grid.setRowMinimumHeight(0, 40)
        layout_grid.setRowMinimumHeight(1, 40)
        layout_grid.setColumnStretch(2, 50)
        layout_grid.setColumnStretch(5, 50)
        layout_main.addLayout(layout_grid)
        layout_main.addSpacing(15)

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
    widget.resize(1400, 900)
    widget.show()
    sys.exit(app.exec())


