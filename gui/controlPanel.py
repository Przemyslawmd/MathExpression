
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QComboBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSlider

from color import Colors


def create_button(label, width, func=None):
    button = QPushButton(label)
    button.setMaximumWidth(width)
    button.setMinimumWidth(width)
    button.clicked.connect(func)
    return button


def create_layout_for_widget_and_label(widget, width, text, text_width, alignment=None, default_value=""):
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
        self.y_min = QLineEdit()
        self.y_max = QLineEdit()
        self.coordinates = QLineEdit()
        self.pen_width = QComboBox()
        self.box_pen_colors = QComboBox()
        self.current_pen_color = (0, 255, 128)
        self.ratio_slider = QSlider()
        self.ratio_label = QLabel()
        self.ratio_values = (
            0.1, 0.11, 0.125, 0.15, 0.2, 0.25, 0.33, 0.5, 0.65, 0.75, 0.85, 1, 1.15, 1.33, 1.5, 2, 3, 4, 5, 7, 8, 9, 10
        )


    def on_box_pen_colors_changed(self, color_text):
        self.current_pen_color = next((color.rgb for color in Colors.values() if color.text == color_text), None)


    def create_first_row(self, layout, func_draw, func_append, x_min, x_max):
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(create_button("Draw Graph", 140, func_draw), 0, 0)
        layout.addWidget(create_button("Append Graph", 140, func_append), 0, 1)
        layout.setSpacing(15)

        widget_with_label = create_layout_for_widget_and_label(self.x_min, 40, "X Min", 40, Qt.AlignCenter, str(x_min))
        layout.addLayout(widget_with_label, 0, 3)

        widget_with_label = create_layout_for_widget_and_label(self.x_max, 40, "X Max", 40, Qt.AlignCenter, str(x_max))
        layout.addLayout(widget_with_label, 0, 4)

        [self.pen_width.addItem(str(x))
         for x in (0.1, 0.2, 0.3, 0.4, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 7, 8, 9, 10)]
        self.pen_width.setCurrentIndex(4)
        widget_with_label = create_layout_for_widget_and_label(self.pen_width, 100, "Line Width", 65)
        layout.addLayout(widget_with_label, 0, 6)

        layout_ratio = QHBoxLayout()
        layout_ratio.setSpacing(8)
        label = QLabel("Y : X Ratio")
        label.setFixedSize(60, 10)

        self.ratio_slider.setMinimum(0)
        self.ratio_slider.setMaximum(22)
        self.ratio_slider.setSingleStep(1)
        self.ratio_slider.setOrientation(Qt.Horizontal)
        self.ratio_slider.setValue(11)
        ratio = self.ratio_values[self.ratio_slider.value()]
        self.ratio_label.setText(str(ratio))

        button = create_button("Default", 80, lambda: self.ratio_slider.setValue(11))

        layout_ratio.addWidget(label)
        layout_ratio.addWidget(self.ratio_slider)
        layout_ratio.addWidget(self.ratio_label)
        layout_ratio.addWidget(button)

        layout.addLayout(layout_ratio, 0, 8)


    def create_second_row(self, layout, func_clear_insert, func_clear_plot):
        layout.addWidget(create_button("Clear Insert Area", 140, func_clear_insert), 1, 0)
        layout.addWidget(create_button("Clear Plot Area", 140, func_clear_plot), 1, 1)

        widget_with_label = create_layout_for_widget_and_label(self.y_min, 40, "Y Min", 40, Qt.AlignCenter)
        layout.addLayout(widget_with_label, 1, 3)

        widget_with_label = create_layout_for_widget_and_label(self.y_max, 40, "Y Max", 40, Qt.AlignCenter)
        layout.addLayout(widget_with_label, 1, 4)

        [self.box_pen_colors.addItem(value.text) for value in Colors.values()]
        self.box_pen_colors.setCurrentIndex(4)
        self.box_pen_colors.currentTextChanged.connect(self.on_box_pen_colors_changed)
        widget_with_label = create_layout_for_widget_and_label(self.box_pen_colors, 100, "Line Color", 65)
        layout.addLayout(widget_with_label, 1, 6)

        widget_with_label = create_layout_for_widget_and_label(self.coordinates, 420, "Coordinate", 70, Qt.AlignRight)
        widget_with_label.setAlignment(Qt.AlignLeft)
        layout.addLayout(widget_with_label, 1, 8)


    def connect_slider(self, func):
        self.ratio_slider.valueChanged.connect(func)


