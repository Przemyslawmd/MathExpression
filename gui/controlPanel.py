
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QComboBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSlider

from color import Colors


def create_button(label, width, func = None) -> QPushButton:
    button = QPushButton(label)
    button.setMaximumWidth(width)
    button.setMinimumWidth(width)
    button.clicked.connect(func)
    return button


def create_layout(widget, width, text, text_width, alignment = None, default_value = None) -> QHBoxLayout:
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


def prepare_axis_slider(slider) -> None:
    slider.setMinimum(0)
    slider.setMaximum(22)
    slider.setSingleStep(1)
    slider.setOrientation(Qt.Orientation.Horizontal)
    slider.setValue(11)
    slider.setFixedWidth(300)
    slider.setEnabled(False)


class ControlPanel:

    def __init__(self):
        self.x_min = QLineEdit()
        self.x_max = QLineEdit()
        self.y_view = QLineEdit()
        self.pen_width = QComboBox()
        self.pen_colors = QComboBox()
        self.current_pen_color = (0, 255, 128)
        self.x_axis = QSlider()
        self.y_axis = QSlider()


    def create_first_row(self, layout, func_draw, func_append) -> None:
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(create_button("Draw Graph", 140, func_draw), 0, 0)
        layout.addWidget(create_button("Append Graph", 140, func_append), 0, 1)
        layout.setSpacing(15)

        layout_x_min = create_layout(self.x_min, 40, "X Min", 40, Qt.AlignmentFlag.AlignCenter, "-360")
        layout.addLayout(layout_x_min, 0, 3)

        layout_x_max = create_layout(self.x_max, 40, "X Max", 40, Qt.AlignmentFlag.AlignCenter, "360")
        layout.addLayout(layout_x_max, 0, 4)

        for x in (0.1, 0.2, 0.3, 0.4, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 7, 8, 9, 10):
            self.pen_width.addItem(str(x))
        self.pen_width.setCurrentIndex(4)
        layout_pen_width = create_layout(self.pen_width, 100, "Line Width", 75)
        layout.addLayout(layout_pen_width, 0, 6)

        layout_ratio = QHBoxLayout()
        layout_ratio.setSpacing(8)
        label = QLabel("X Axis Range")
        label.setFixedSize(90, 17)
        prepare_axis_slider(self.x_axis)
        button_x_axis = create_button("Default", 80, lambda: self.x_axis.setValue(11))

        layout_ratio.addWidget(label)
        layout_ratio.addWidget(self.x_axis)
        layout_ratio.addWidget(button_x_axis)
        layout.addLayout(layout_ratio, 0, 8)


    def create_second_row(self, layout, func_clear_insert, func_clear_plot) -> None:
        layout.addWidget(create_button("Clear Insert Area", 140, func_clear_insert), 1, 0)
        layout.addWidget(create_button("Clear Plot Area", 140, func_clear_plot), 1, 1)

        layout_y_view = create_layout(self.y_view, 105, "Y View", 85, Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(layout_y_view, 1, 3, 1, 2)

        for color in Colors.values():
            self.pen_colors.addItem(color.text)
        self.pen_colors.setCurrentIndex(4)
        self.pen_colors.currentTextChanged.connect(self.on_pen_colors_changed)
        layout_pen_color = create_layout(self.pen_colors, 100, "Line Color", 75)
        layout.addLayout(layout_pen_color, 1, 6)

        layout_ratio = QHBoxLayout()
        layout_ratio.setSpacing(8)
        label = QLabel("Y Axis Range")
        label.setFixedSize(90, 17)
        prepare_axis_slider(self.y_axis)
        button_y_axis = create_button("Default", 80, lambda: self.y_axis.setValue(11))

        layout_ratio.addWidget(label)
        layout_ratio.addWidget(self.y_axis)
        layout_ratio.addWidget(button_y_axis)
        layout.addLayout(layout_ratio, 1, 8)


    def connect_sliders(self, func_x, func_y) -> None:
        self.x_axis.valueChanged.connect(func_x)
        self.y_axis.valueChanged.connect(func_y)


    def reset_sliders(self) -> None:
        self.x_axis.setEnabled(True)
        self.y_axis.setEnabled(True)
        self.x_axis.setValue(11)
        self.y_axis.setValue(11)

    # ------------------------------- INTERNAL ----------------------------------- #

    def on_pen_colors_changed(self, color_text) -> None:
        self.current_pen_color = next((color.rgb for color in Colors.values() if color.text == color_text), None)

