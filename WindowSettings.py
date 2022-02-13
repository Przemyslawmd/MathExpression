
from PySide6 import QtCore
from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QDialog, QGridLayout, QHBoxLayout, QVBoxLayout, QCheckBox, QComboBox, QLabel, QPushButton


class WindowSettings(QDialog):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 30, 0)

        layout_grid = QGridLayout()
        layout_grid.addWidget(QLabel("X Grid"), 1, 1)
        self.check_x_grid = QCheckBox()
        self.check_x_grid.setChecked(self.parent.x_grid)
        layout_grid.addWidget(self.check_x_grid, 1, 2, alignment=QtCore.Qt.AlignRight)
        layout_grid.setRowMinimumHeight(1, 30)

        layout_grid.addWidget(QLabel("Y Grid"), 2, 1)
        self.check_y_grid = QCheckBox()
        self.check_y_grid.setChecked(self.parent.y_grid)
        layout_grid.addWidget(self.check_y_grid, 2, 2, alignment=QtCore.Qt.AlignRight)
        layout_grid.setRowMinimumHeight(2, 30)

        layout_grid.addWidget(QLabel("X Precision"), 3, 1)
        self.insert_x_precision = QComboBox()
        self.insert_x_precision.setMaximumWidth(60)
        index = 0
        for i in [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0]:
            self.insert_x_precision.addItem(str(i))
            if i == self.parent.x_precision:
                self.insert_x_precision.setCurrentIndex(index)
            index += 1
        layout_grid.addWidget(self.insert_x_precision, 3, 2, alignment=QtCore.Qt.AlignRight)
        layout.addLayout(layout_grid)

        layout_button = QHBoxLayout()
        layout_button.addStretch()
        button = QPushButton("Accept")
        button.clicked.connect(lambda: self.accept())
        layout_button.addWidget(button)
        layout_button.addStretch()

        layout.addLayout(layout_button)
        self.setMinimumWidth(250)
        self.setMinimumHeight(210)
        self.setWindowModality(Qt.ApplicationModal)
        self.setLayout(layout)
        self.setGeometry(400, 400, 0, 0)
        self.show()
        self.exec()


    @Slot()
    def accept(self):
        self.parent.apply_settings(self.check_x_grid.isChecked(),
                                   self.check_y_grid.isChecked(),
                                   float(self.insert_x_precision.currentText()))
        self.close()


