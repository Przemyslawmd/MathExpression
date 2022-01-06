
import sys

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QVBoxLayout, QLabel, QWidget


class WindowAbout(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 40, 0, 0)
        label = QLabel("Author:          przemyslawmd@gmail.com")
        label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        layout.addWidget(label)
        layout.addSpacing(20)
        label = QLabel("Web page:     www.przemeknet.pl")
        label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        layout.addWidget(label)
        layout.addStretch()

        self.setMinimumWidth(400)
        self.setMinimumHeight(150)
        self.setWindowModality(Qt.ApplicationModal)
        self.setLayout(layout)
        self.setGeometry(400, 400, 0, 0)
        self.show()
        sys.exit(self.exec_())

