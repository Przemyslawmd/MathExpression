
from PySide2 import QtCore
from PySide2.QtCore import Qt, Slot
from PySide2.QtWidgets import QVBoxLayout, QLabel, QWidget, QPushButton, QGridLayout, QCheckBox, QHBoxLayout


class WindowSettings(QWidget):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 30, 0)

        layout_grid = QGridLayout()
        layout_grid.addWidget(QLabel("X Grid"), 1, 1)
        self.check_x_grid = QCheckBox()
        self.check_x_grid.setGeometry(100, 50, 10, 10)
        self.check_x_grid.setChecked(self.parent.x_grid)
        layout_grid.addWidget(self.check_x_grid, 1, 2, alignment=QtCore.Qt.AlignRight)
        layout_grid.addWidget(QLabel("Y Grid"), 2, 1)
        self.check_y_grid = QCheckBox()
        self.check_y_grid.setChecked(self.parent.y_grid)
        layout_grid.addWidget(self.check_y_grid, 2, 2, alignment=QtCore.Qt.AlignRight)
        layout.addLayout(layout_grid)

        layout_button = QHBoxLayout()
        layout_button.addStretch()
        button = QPushButton("Accept")
        button.clicked.connect(lambda: self.accept())
        layout_button.addWidget(button)
        layout_button.addStretch()

        layout.addLayout(layout_button)
        self.setMinimumWidth(200)
        self.setMinimumHeight(150)
        self.setWindowModality(Qt.ApplicationModal)
        self.setLayout(layout)
        self.setGeometry(400, 400, 0, 0)
        self.show()
        self.exec_()


    @Slot()
    def accept(self):
        self.parent.apply_settings(self.check_x_grid.isChecked(), self.check_y_grid.isChecked())
        self.close()


