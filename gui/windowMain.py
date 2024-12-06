
from collections import namedtuple
from PySide6.QtCore import Slot
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QGridLayout, QMainWindow, QLineEdit, QTextEdit, QToolBar, QVBoxLayout, QWidget
from numpy import arange
from pyqtgraph import PlotWidget, mkPen
import pyqtgraph as pg

from color import Colors
from controller import calculate_values
from errors import Error, Message
from errorStorage import ErrorStorage
from settings import Settings
from gui.controlPanel import ControlPanel
from gui.utils import max_points_exceeded, calculate_range_x, calculate_axis_change
from gui.windowAbout import WindowAbout
from gui.windowSettings import WindowSettings


Line = namedtuple("PlotLine", "data expression")


class MathExpression(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        self.panel = ControlPanel()
        self.settings = Settings()
        self.plot_widget = PlotWidget()
        self.insert_expression = QLineEdit()
        self.area_messages = QTextEdit()
        self.plot_lines = []
        self.setWindowTitle(' ')
        self.legend = pg.LegendItem((50, 100), offset=(50, 20))
        self.axis_x = None
        self.axis_y = None


    @Slot()
    def draw(self):
        self.clear_plot_area()
        self.create_graph()


    @Slot()
    def append(self):
        if len(self.plot_lines) == 10:
            self.print_message("Only ten graphs allowed")
            return
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
        self.panel.x_axis.setEnabled(False)
        self.panel.y_axis.setEnabled(False)


    @Slot()
    def widget_settings(self):
        WindowSettings(self, self.settings)


    @Slot()
    def window_about(self):
        WindowAbout()


    @Slot()
    def change_axis_x(self):
        x_min, x_max = self.axis_x
        change = calculate_axis_change(self.panel.x_axis, x_min, x_max)
        self.plot_widget.setXRange(x_min - change, x_max + change)


    @Slot()
    def change_axis_y(self):
        y_min, y_max = self.axis_y
        change = calculate_axis_change(self.panel.y_axis, y_min, y_max)
        self.plot_widget.setYRange(y_min - change, y_max + change)


    def print_message(self, message: str):
        self.area_messages.clear()
        self.area_messages.setText(message)


    def print_message_from_storage(self):
        self.area_messages.clear()
        for error in ErrorStorage.get_errors():
            self.area_messages.setText(error)


    def add_graph_label(self):
        if self.settings.graph_label is False:
            return
        self.legend.clear()
        self.legend.setParentItem(self.plot_widget.plotItem)
        for plot in self.plot_lines:
            self.legend.addItem(plot.data, plot.expression)


    def create_graph(self):
        ErrorStorage.clear()
        min_str = self.panel.x_min.text().lstrip()
        max_str = self.panel.x_max.text().lstrip()

        x_min, x_max = calculate_range_x(min_str, max_str)
        if x_min is None:
            self.print_message_from_storage()
            return
        precision = self.settings.precision
        if max_points_exceeded(precision, x_min, x_max):
            self.print_message(Message[Error.MAX_POINTS])
            return

        y_values = calculate_values(self.insert_expression.text(), x_min, x_max, precision)
        if y_values is None:
            self.print_message_from_storage()
            return

        x_values = arange(x_min, x_max + precision, precision)
        line_width = float(self.panel.pen_width.currentText())
        line_color = self.panel.current_pen_color
        plot_pen = mkPen(line_color, width=line_width)
        plot = self.plot_widget.plot(x_values, y_values, pen=plot_pen, symbol='x', symbolPen=None, symbolBrush=2.5, connect="finite")
        line = Line(plot, self.insert_expression.text())
        self.plot_lines.append(line)
        self.add_graph_label()
        self.area_messages.clear()

        self.axis_x = [x_min, x_max]
        self.axis_y = [min(y_values), max(y_values)]
        self.plot_widget.setXRange(x_min, x_max)
        self.plot_widget.setYRange(self.axis_y[0], self.axis_y[1])
        self.panel.reset_sliders()


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
        self.insert_expression.setTextMargins(5, 0, 0, 0)
        lay_main.addWidget(self.insert_expression)
        lay_main.addSpacing(10)

        lay_panel = QGridLayout()
        self.panel.create_first_row(lay_panel, lambda: self.draw(), lambda: self.append())
        self.panel.create_second_row(lay_panel, lambda: self.clear_insert_area(), lambda: self.clear_plot_area())

        self.panel.connect_sliders(self.change_axis_x, self.change_axis_y)

        lay_panel.setRowMinimumHeight(0, 40)
        lay_panel.setRowMinimumHeight(1, 40)
        lay_panel.setColumnStretch(2, 25)
        lay_panel.setColumnStretch(5, 25)
        lay_panel.setColumnStretch(7, 25)

        panel_widget = QWidget()
        panel_widget.setMaximumWidth(1400)
        panel_widget.setLayout(lay_panel)
        lay_main.addWidget(panel_widget)
        lay_main.addSpacing(15)

        self.plot_widget.showGrid(x=self.settings.x_grid, y=self.settings.y_grid)
        self.plot_widget.setStyleSheet("border: 1px solid black")
        lay_main.addWidget(self.plot_widget)
        lay_main.addSpacing(20)

        lay_main.addWidget(self.area_messages)
        self.area_messages.setMaximumHeight(60)
        lay_main.addSpacing(20)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_widget.setLayout(lay_main)
        main_widget.setContentsMargins(20, 0, 20, 0)


    def apply_settings(self, grid_changed, background_changed):
        if grid_changed is True:
            self.plot_widget.showGrid(x=self.settings.x_grid, y=self.settings.y_grid)
        if background_changed is True:
            self.plot_widget.setBackground(Colors[self.settings.background].text)

