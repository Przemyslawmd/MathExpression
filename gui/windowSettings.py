
from PySide6 import QtCore
from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QDialog, QGridLayout, QHBoxLayout, QVBoxLayout, QCheckBox, QComboBox, QLabel, QPushButton

from color import Colors


class WindowSettings(QDialog):

    def __init__(self, parent, settings):
        super().__init__()

        self.parent = parent
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 30, 0)

        layout_grid = QGridLayout()

        layout_grid.addWidget(QLabel("X Grid"), 1, 1)
        self.check_x_grid = QCheckBox()
        self.check_x_grid.setChecked(settings.x_grid)
        layout_grid.addWidget(self.check_x_grid, 1, 2, alignment=QtCore.Qt.AlignRight)

        layout_grid.addWidget(QLabel("Y Grid"), 2, 1)
        self.check_y_grid = QCheckBox()
        self.check_y_grid.setChecked(settings.y_grid)
        layout_grid.addWidget(self.check_y_grid, 2, 2, alignment=QtCore.Qt.AlignRight)

        layout_grid.addWidget(QLabel("Display Coordinates"), 3, 1)
        self.check_coordinates = QCheckBox()
        self.check_coordinates.setChecked(settings.coordinates)
        layout_grid.addWidget(self.check_coordinates, 3, 2, alignment=QtCore.Qt.AlignRight)

        layout_grid.addWidget(QLabel("Graph Label"), 4, 1)
        self.check_label = QCheckBox()
        self.check_label.setChecked(settings.graph_label)
        layout_grid.addWidget(self.check_label, 4, 2, alignment=QtCore.Qt.AlignRight)

        layout_grid.addWidget(QLabel("Precision"), 5, 1)
        self.combo_precision = QComboBox()
        self.combo_precision.setMaximumWidth(100)
        for i, precision in enumerate((0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0)):
            self.combo_precision.addItem(str(precision))
            if precision == settings.precision:
                self.combo_precision.setCurrentIndex(i)
        layout_grid.addWidget(self.combo_precision, 5, 2, alignment=QtCore.Qt.AlignRight)

        layout_grid.addWidget(QLabel("Background Color"), 6, 1)
        self.combo_background = QComboBox()
        self.combo_background.setMaximumWidth(120)
        [self.combo_background.addItem(value.text) for value in Colors.values()]
        self.combo_background.setCurrentText(Colors[settings.background].text)
        layout_grid.addWidget(self.combo_background, 6, 2, alignment=QtCore.Qt.AlignRight)

        for row in range(1, layout_grid.rowCount()):
            layout_grid.setRowMinimumHeight(row, 30)

        layout.addLayout(layout_grid)

        layout_button = QHBoxLayout()
        layout_button.addStretch()
        button = QPushButton("Accept")
        button.clicked.connect(lambda: self.accept(settings))
        layout_button.addWidget(button)
        layout_button.addStretch()

        layout.addLayout(layout_button)
        self.setMinimumWidth(320)
        self.setMinimumHeight(320)
        self.setWindowModality(Qt.ApplicationModal)
        self.setLayout(layout)
        self.setGeometry(550, 500, 0, 0)
        self.show()
        self.exec()


    @Slot()
    def accept(self, settings):

        grid, background, coordinates = settings.set_settings(self.check_x_grid.isChecked(),
                                                              self.check_y_grid.isChecked(),
                                                              float(self.combo_precision.currentText()),
                                                              self.check_coordinates.isChecked(),
                                                              self.combo_background.currentText(),
                                                              self.check_label.isChecked())
        self.parent.apply_settings(grid, background, coordinates)
        self.close()


