
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QComboBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSlider

from color import Colors


def create_button(label, width, func=None):
    button = QPushButton(label)
    button.setMaximumWidth(width)
    button.setMinimumWidth(width)
    button.clicked.connect(func)
    return button


def create_widget_layout(widget, width, text, text_width, alignment=None, default_value=None):
    widget.setMinimumWidth(width)
    widget.setMaximumWidth(width)
    if isinstance(widget, QLineEdit):
        widget.setText(default_value)
    if alignment is not None:
        widget.setAlignment(alignment)
    label = QLabel(text)
    label.setFixedSize(text_width, 10)
    label.setMargin(0)
    layout = QHBoxLayout()
    layout.addWidget(label)
    layout.setSpacing(5)
    layout.addWidget(widget)
    return layout


class ControlPanel:

    def __init__(self):
        self.x_min = QLineEdit()
        self.x_max = QLineEdit()
        self.pen_width = QComboBox()
        self.pen_colors = QComboBox()
        self.current_pen_color = (0, 255, 128)
        self.x_axis = QSlider()
        self.x_axis_values = (
            0.1, 0.11, 0.125, 0.15, 0.2, 0.25, 0.33, 0.5, 0.65, 0.75, 0.85, 1, 1.15, 1.33, 1.5, 2, 3, 4, 5, 7, 8, 9, 10
        )


    def create_first_row(self, layout, func_draw, func_append):
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(create_button("Draw Graph", 140, func_draw), 0, 0)
        layout.addWidget(create_button("Append Graph", 140, func_append), 0, 1)
        layout.setSpacing(15)

        widget_x_min = create_widget_layout(self.x_min, 40, "X Min", 40, Qt.AlignmentFlag.AlignCenter, "-360")
        layout.addLayout(widget_x_min, 0, 3)

        widget_x_max = create_widget_layout(self.x_max, 40, "X Max", 40, Qt.AlignmentFlag.AlignCenter, "360")
        layout.addLayout(widget_x_max, 0, 4)

        for x in (0.1, 0.2, 0.3, 0.4, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 7, 8, 9, 10):
            self.pen_width.addItem(str(x))
        self.pen_width.setCurrentIndex(4)
        widget_pen_width = create_widget_layout(self.pen_width, 100, "Line Width", 65)
        layout.addLayout(widget_pen_width, 0, 6)

        layout_ratio = QHBoxLayout()
        layout_ratio.setSpacing(8)
        label = QLabel("X Axis Range")
        label.setFixedSize(80, 17)

        self.x_axis.setMinimum(0)
        self.x_axis.setMaximum(22)
        self.x_axis.setSingleStep(1)
        self.x_axis.setOrientation(Qt.Orientation.Horizontal)
        self.x_axis.setValue(11)
        self.x_axis.setFixedWidth(300)
        self.x_axis.setEnabled(False)

        button_x_axis = create_button("Default", 80, lambda: self.x_axis.setValue(11))

        layout_ratio.addWidget(label)
        layout_ratio.addWidget(self.x_axis)
        layout_ratio.addWidget(button_x_axis)
        layout.addLayout(layout_ratio, 0, 8)


    def create_second_row(self, layout, func_clear_insert, func_clear_plot):
        layout.addWidget(create_button("Clear Insert Area", 140, func_clear_insert), 1, 0)
        layout.addWidget(create_button("Clear Plot Area", 140, func_clear_plot), 1, 1)

        for color in Colors.values():
            self.pen_colors.addItem(color.text)
        self.pen_colors.setCurrentIndex(4)
        self.pen_colors.currentTextChanged.connect(self.on_pen_colors_changed)
        widget_pen_color = create_widget_layout(self.pen_colors, 100, "Line Color", 65)
        layout.addLayout(widget_pen_color, 1, 6)


    def connect_slider(self, func):
        self.x_axis.valueChanged.connect(func)


    def reset_slider(self):
        self.x_axis.setEnabled(True)
        self.x_axis.setValue(11)

    # ------------------------------- INTERNAL ----------------------------------- #

    def on_pen_colors_changed(self, color_text):
        self.current_pen_color = next((color.rgb for color in Colors.values() if color.text == color_text), None)

