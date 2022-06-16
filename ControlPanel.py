
from PySide6.QtWidgets import QLabel, QComboBox
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QPushButton, QLineEdit
from PySide6.QtGui import Qt


class ControlPanel:

    def __init__(self):
        self.x_min = QLineEdit()
        self.x_max = QLineEdit()
        self.y_min = QLineEdit()
        self.y_max = QLineEdit()
        self.pen_width = QComboBox()
        self.pen_color = QComboBox()
        self.ratio_buttons = []

        self.colors = {
            "Black": [0, 0, 0], "Blue": [0, 0, 255], "Green": [0, 128, 0], "Light Blue": [0, 191, 255],
            "Light Green": [0, 255, 128], "Orange": [255, 140, 0], "Red": [255, 0, 0],
            "Yellow": [255, 255, 0], "White": [255, 255, 255]
        }

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


    def create_first_row(self, layout, func_draw, func_append, x_min, x_max):
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


    def create_second_row(self, layout, func_clear_insert, func_clear_plot):
        layout.addWidget(self.create_button("Clear Insert Area", 140, func_clear_insert), 1, 0)
        layout.addWidget(self.create_button("Clear Plot Area", 140, func_clear_plot), 1, 1)

        widget_with_label = self.create_widget_with_label(self.y_min, 40, "Y Min", 40)
        layout.addLayout(widget_with_label, 1, 3)

        widget_with_label = self.create_widget_with_label(self.y_max, 40, "Y Max", 40)
        layout.addLayout(widget_with_label, 1, 4)

        self.pen_color.addItems(["Black", "Blue", "Green", "Light Blue", "Light Green", "Orange", "Red", "White",
                                 "Yellow"])
        self.pen_color.setCurrentIndex(4)
        widget_with_label = self.create_widget_with_label(self.pen_color, 100, "Line Color", 65)
        layout.addLayout(widget_with_label, 1, 6)


    def connect_ratio_button(self, index, func):
        self.ratio_buttons[index].clicked.connect(func)


    def get_current_color(self):
        return self.colors[self.pen_color.currentText()]


