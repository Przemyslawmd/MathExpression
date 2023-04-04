
import sys
from collections import namedtuple
from PySide6.QtCore import Slot
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QToolBar
from PySide6.QtWidgets import QLineEdit, QTextEdit
from PySide6.QtWidgets import QVBoxLayout, QGridLayout
from numpy import arange
from pyqtgraph import PlotWidget, mkPen
import pyqtgraph as pg

from color import Colors
from controlPanel import ControlPanel
from controller import Controller
from errors import Error, ErrorMessage
from settings import Settings
from utils import is_max_points_exceeded, calculate_range, RangeType
from windowAbout import WindowAbout
from windowSettings import WindowSettings


Line = namedtuple("PlotLine", "data expression")


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
        self.setWindowTitle(' ')
        self.legend = pg.LegendItem((50, 100), offset=(50, 20))

        self.x_min = -360
        self.x_max = 360
        self.ratio_buttons = None


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
            self.plot_widget.removeItem(line.data)
        self.plot_lines.clear()
        if self.settings.graph_label:
            self.legend.clear()


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


    def mouse_moved(self, evt):
        x = round(self.plot_widget.plotItem.vb.mapSceneToView(evt).x(), 3)
        y = round(self.plot_widget.plotItem.vb.mapSceneToView(evt).y(), 3)
        self.panel.coordinates.setText(f"  X: {str(x)}  ;  Y: {str(y)} ")


    def create_graph(self):
        min_str = self.panel.x_min.text().lstrip()
        max_str = self.panel.x_max.text().lstrip()
        try:
            x_min, x_max = calculate_range(min_str, max_str, RangeType.X)
        except Exception as e:
            self.set_message(str(e))
            return
        precision = self.settings.precision
        if is_max_points_exceeded(precision, x_min, x_max):
            self.set_message(ErrorMessage[Error.MAX_POINTS])
            return
        min_str = self.panel.y_min.text().lstrip()
        max_str = self.panel.y_max.text().lstrip()
        try:
            y_min, y_max = calculate_range(min_str, max_str, RangeType.Y)
        except Exception as e:
            self.set_message(str(e))
            return
        if y_min != 0 and y_max != 0:
            self.plot_widget.setYRange(y_min, y_max, padding=0)

        try:
            y = self.controller.calculate_values(self.insert_expression.text(), x_min, x_max, precision)
        except Exception as e:
            self.set_message(str(e))
            return

        x = arange(x_min, x_max + precision, precision)
        line_width = float(self.panel.pen_width.currentText())
        line_color = self.panel.current_pen_color
        plot = self.plot_widget.plot(x, y, pen=mkPen(line_color, width=line_width), symbol='x',
                                     symbolPen=None, symbolBrush=2.5, connect="finite")

        self.plot_widget.setBackground(Colors[self.settings.background].text)

        line = Line(plot, self.insert_expression.text())
        self.plot_lines.append(line)

        if self.settings.graph_label:
            self.legend.clear()
            self.legend.setParentItem(self.plot_widget.plotItem)
            [self.legend.addItem(plot.data, plot.expression) for plot in self.plot_lines]
        self.area_messages.clear()


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
        if self.settings.background_changed is True:
            self.plot_widget.setBackground(Colors[self.settings.background].text)
        if self.settings.coordinates_changed is True and self.settings.coordinates is True:
            self.plot_widget.scene().sigMouseMoved.connect(self.mouse_moved)
        elif self.settings.coordinates_changed is True and self.settings.coordinates is False:
            self.plot_widget.scene().sigMouseMoved.disconnect(self.mouse_moved)
            self.panel.coordinates.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MathExpression()
    widget.create_gui()
    widget.resize(1400, 900)
    widget.show()
    sys.exit(app.exec())


