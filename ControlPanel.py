
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QMainWindow, QToolBar
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout
from PySide6.QtWidgets import QPushButton, QLineEdit, QTextEdit
from PySide6.QtCore import Slot
from PySide6.QtGui import Qt, QAction


class ControlPanel:

    def __init__(self):
        self.x_min = QLineEdit()
        self.x_max = QLineEdit()
        self.pen_width = QComboBox()
        self.ratio_buttons = None


    @staticmethod
    def create_button(label, width, func=None):
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


    def create_upper_row(self, layout, func_draw, func_append, x_min, x_max):
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.create_button("Draw Graph", 140, func_draw), 0, 0)
        layout.addWidget(self.create_button("Append Graph", 140, func_append), 0, 1)
        layout.setSpacing(15)

        widget_with_label = self.create_widget_with_label(self.x_min, 40, "X Min", 40, str(x_min))
        layout.addLayout(widget_with_label, 0, 3)

        widget_with_label = self.create_widget_with_label(self.x_max, 40, "X Max", 40, str(x_max))
        layout.addLayout(widget_with_label, 0, 4)

        [self.pen_width.addItem(str(x))
        for x in [0.1, 0.2, 0.3, 0.4, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 7, 8, 9, 10]]
        self.pen_width.setCurrentIndex(4)
        widget_with_label = self.create_widget_with_label(self.pen_width, 100, "Line Width", 65)
        layout.addLayout(widget_with_label, 0, 6)

        lay_hor = QHBoxLayout()
        lay_hor.setSpacing(8)
        label = QLabel("X : Y Ratio")
        label.setFixedSize(60, 10)
        lay_hor.addWidget(label)

        #self.ratio_buttons = [self.create_button("8/1", 50, lambda: self.change_x_y_ratio(0.125, 0)),
        #                      self.create_button("4/1", 50, lambda: self.change_x_y_ratio(0.25, 1)),
        #                      self.create_button("2/1", 50, lambda: self.change_x_y_ratio(0.5, 2)),
        #                      self.create_button("1/1", 50, lambda: self.change_x_y_ratio(1, 3)),
        #                      self.create_button("1/2", 50, lambda: self.change_x_y_ratio(2, 4)),
        #                      self.create_button("1/4", 50, lambda: self.change_x_y_ratio(4, 5)),
        #                      self.create_button("1/8", 50, lambda: self.change_x_y_ratio(8, 6))]
        #[lay_hor.addWidget(button) for button in self.ratio_buttons]

        self.ratio_buttons = [self.create_button("8/1", 50),
                              self.create_button("4/1", 50),
                              self.create_button("2/1", 50),
                              self.create_button("1/1", 50),
                              self.create_button("1/2", 50),
                              self.create_button("1/4", 50),
                              self.create_button("1/8", 50)]
        [lay_hor.addWidget(button) for button in self.ratio_buttons]

        self.ratio_buttons[3].setStyleSheet("background-color : #b3b3b3")
        layout.addLayout(lay_hor, 0, 8)

