
import sys

from numpy import arange

from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QToolBar
from PySide6.QtWidgets import QVBoxLayout, QGridLayout
from PySide6.QtWidgets import QLineEdit, QTextEdit
from PySide6.QtCore import Slot
from PySide6.QtGui import QAction
from pyqtgraph import PlotWidget, mkPen

from Errors import ErrorType, ErrorMessage
from Controller import Controller
from ControlPanel import ControlPanel
from Settings import Settings
from WindowAbout import WindowAbout
from WindowSettings import WindowSettings


class MathExpression(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        self.controller = Controller()
        self.panel = ControlPanel()
        self.settings = Settings()
        self.plot_widget = PlotWidget()
        self.insert_expression = QLineEdit()
        self.area_messages = QTextEdit()
        self.plot_lines = []

        self.x_min = -360
        self.x_max = 360
        self.MAX_POINTS = 100000
        self.ratio_buttons = None

        self.create_gui()


    @Slot()
    def draw(self):
        self.clear_plot_area()
        self.create_graph()


    @Slot()
    def append(self):
        self.create_graph()


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
        WindowSettings(self, self.settings)


    @Slot()
    def window_about(self):
        WindowAbout()


    @Slot()
    def change_ratio(self, ratio, index):
        self.plot_widget.setXRange(self.x_min * ratio, self.x_max * ratio)
        [x.setStyleSheet("") for x in self.panel.ratio_buttons]
        self.panel.ratio_buttons[index].setStyleSheet("background-color : #b3b3b3")


    def set_message(self, message):
        self.area_messages.clear()
        self.area_messages.setText(message)


    def is_max_points_exceeded(self, x_min, x_max, precision):
        if x_min >= 0 and x_max >= 0:
            return (x_max - x_min) / precision > self.MAX_POINTS
        if x_min < 0 and x_max < 0:
            return (x_min - x_max) * -1 / precision > self.MAX_POINTS
        return (x_max + x_min * -1) / precision > self.MAX_POINTS


    def mouse_moved(self, evt):
        x = round(self.plot_widget.plotItem.vb.mapSceneToView(evt).x(), 3)
        y = round(self.plot_widget.plotItem.vb.mapSceneToView(evt).y(), 3)
        self.panel.coordinates.setText(f"  X: {str(x)}  ;  Y: {str(y)} ")


    def create_graph(self):
        self.x_min, self.x_max = self.calculate_range(self.panel.x_min, self.panel.x_max)
        precision = self.settings.precision
        if self.x_min == 0 and self.x_max == 0:
            return
        if self.is_max_points_exceeded(self.x_min, self.x_max, precision):
            self.set_message(ErrorMessage[ErrorType.MAX_POINTS])
            return
        if self.panel.y_min.text() or self.panel.y_max.text():
            if self.panel.y_min.text() and self.panel.y_max.text():
                y_min, y_max = self.calculate_range(self.panel.y_min, self.panel.y_max)
                if y_min == 0 and y_max == 0:
                    return
                self.plot_widget.setYRange(y_min, y_max, padding=0)
            else:
                self.set_message("Range error: only one value for Y range")
                return
        try:
            y = self.controller.calculate_values(self.insert_expression.text(), self.x_min, self.x_max, precision)
        except Exception as e:
            self.set_message(str(e))
            return

        x = arange(self.x_min, self.x_max + precision, precision)
        line_width = float(self.panel.pen_width.currentText())
        line_color = self.panel.current_pen_color
        plot = self.plot_widget.plot(x, y, pen=mkPen(line_color, width=line_width), symbol='x',
                                     symbolPen=None, symbolBrush=2.5, connect="finite")

        self.plot_widget.setBackground(self.settings.background_color)
        self.plot_lines.append(plot)
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


    def create_gui(self):
        tool_bar = QToolBar()
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(lambda: self.widget_settings())
        tool_bar.addAction(settings_action)
        about_action = QAction("About", self)
        about_action.triggered.connect(lambda: self.window_about())
        tool_bar.addAction(about_action)
        self.addToolBar(tool_bar)

        lay_main = QVBoxLayout()
        lay_main.addSpacing(20)
        lay_main.addWidget(self.insert_expression)
        lay_main.addSpacing(10)

        lay_grid = QGridLayout()
        self.panel.create_first_row(lay_grid, lambda: self.draw(), lambda: self.append(), self.x_min, self.x_max)
        self.panel.connect_ratio_button(0, lambda: self.change_ratio(0.125, 0))
        self.panel.connect_ratio_button(1, lambda: self.change_ratio(0.25, 1))
        self.panel.connect_ratio_button(2, lambda: self.change_ratio(0.5, 2))
        self.panel.connect_ratio_button(3, lambda: self.change_ratio(1, 3))
        self.panel.connect_ratio_button(4, lambda: self.change_ratio(2, 4))
        self.panel.connect_ratio_button(5, lambda: self.change_ratio(4, 5))
        self.panel.connect_ratio_button(6, lambda: self.change_ratio(8, 6))

        self.panel.create_second_row(lay_grid, lambda: self.clear_insert_area(), lambda: self.clear_plot_area())
        lay_grid.setRowMinimumHeight(0, 40)
        lay_grid.setRowMinimumHeight(1, 40)
        lay_grid.setColumnStretch(2, 25)
        lay_grid.setColumnStretch(5, 25)
        lay_grid.setColumnStretch(7, 25)

        buttons_widget = QWidget()
        buttons_widget.setMaximumWidth(1400)
        buttons_widget.setLayout(lay_grid)
        lay_main.addWidget(buttons_widget)
        lay_main.addSpacing(15)

        self.plot_widget.showGrid(x=self.settings.x_grid, y=self.settings.y_grid)
        self.plot_widget.setStyleSheet("border: 1px solid black")
        lay_main.addWidget(self.plot_widget)
        lay_main.addSpacing(20)

        lay_main.addWidget(self.area_messages)
        self.area_messages.setMaximumHeight(100)
        lay_main.addSpacing(20)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_widget.setLayout(lay_main)
        main_widget.setContentsMargins(20, 0, 20, 0)


    def apply_settings(self):
        if self.settings.grid_changed is True:
            self.plot_widget.showGrid(x=self.settings.x_grid, y=self.settings.y_grid)
        if self.settings.background_color_changed is True:
            self.plot_widget.setBackground(self.settings.background_color)
        if self.settings.coordinates_changed is True and self.settings.coordinates is True:
            self.plot_widget.scene().sigMouseMoved.connect(self.mouse_moved)
        elif self.settings.coordinates_changed is True and self.settings.coordinates is False:
            self.plot_widget.scene().sigMouseMoved.disconnect(self.mouse_moved)
            self.panel.coordinates.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MathExpression()
    widget.resize(1400, 900)
    widget.show()
    sys.exit(app.exec())


