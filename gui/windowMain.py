
from collections import namedtuple
from PySide6.QtCore import Slot
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QGridLayout, QMainWindow, QLineEdit, QTextEdit, QToolBar, QVBoxLayout, QWidget
from numpy import arange
from pyqtgraph import PlotWidget, mkPen
import pyqtgraph as pg

from color import Colors
from controller import calculate_values
from errors import Error, ErrorMessage
from errorStorage import ErrorStorage
from settings import Settings
from gui.controlPanel import ControlPanel
from gui.utils import is_max_points_exceeded, range_x, range_y
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
        self.x_min = -360
        self.x_max = 360


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


    @Slot()
    def widget_settings(self):
        WindowSettings(self, self.settings)


    @Slot()
    def window_about(self):
        WindowAbout()


    @Slot()
    def change_ratio(self):
        slider_index = self.panel.ratio_slider.value()
        ratio = self.panel.ratio_values[slider_index]
        self.plot_widget.setXRange(self.x_min * ratio, self.x_max * ratio)
        self.panel.ratio_label.setText(str(ratio))


    def print_message(self, message: str):
        self.area_messages.clear()
        self.area_messages.setText(message)


    def print_message_from_storage(self):
        self.area_messages.clear()
        for error in ErrorStorage.getErrors():
            self.area_messages.setText(error)


    def mouse_moved(self, evt):
        x = round(self.plot_widget.plotItem.vb.mapSceneToView(evt).x(), 3)
        y = round(self.plot_widget.plotItem.vb.mapSceneToView(evt).y(), 3)
        self.panel.coordinates.setText(f"  X: {str(x)}  ;  Y: {str(y)} ")


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

        x_min, x_max = range_x(min_str, max_str)
        if x_min is None:
            self.print_message_from_storage()
            return
        precision = self.settings.precision
        if is_max_points_exceeded(precision, x_min, x_max):
            self.print_message(ErrorMessage[Error.MAX_POINTS])
            return
        min_str = self.panel.y_min.text().lstrip()
        max_str = self.panel.y_max.text().lstrip()
        y_min, y_max = range_y(min_str, max_str)
        if y_min is None:
            self.print_message_from_storage()
            return
        if y_min != 0 and y_max != 0:
            self.plot_widget.setYRange(y_min, y_max, padding=0)

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
        self.panel.create_second_row(lay_grid, lambda: self.clear_insert_area(), lambda: self.clear_plot_area())

        self.panel.connect_slider(self.change_ratio)

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


    def apply_settings(self, grid_changed, background_changed, coordinates_changed):
        if grid_changed is True:
            self.plot_widget.showGrid(x=self.settings.x_grid, y=self.settings.y_grid)
        if background_changed is True:
            self.plot_widget.setBackground(Colors[self.settings.background].text)
        if coordinates_changed is True and self.settings.coordinates is True:
            self.plot_widget.scene().sigMouseMoved.connect(self.mouse_moved)
        elif coordinates_changed is True and self.settings.coordinates is False:
            self.plot_widget.scene().sigMouseMoved.disconnect(self.mouse_moved)
            self.panel.coordinates.clear()


