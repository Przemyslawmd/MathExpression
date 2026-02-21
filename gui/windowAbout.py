
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout


class WindowAbout(QDialog):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 40, 0, 0)
        label = QLabel("Author:          przemyslawmd@gmail.com")
        label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(label)
        layout.addSpacing(20)
        label = QLabel("Web page:     www.przemeknet.pl/parser.html")
        label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(label)
        layout.addStretch()

        self.setMinimumWidth(350)
        self.setMinimumHeight(150)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setLayout(layout)
        self.show()
        self.exec()


