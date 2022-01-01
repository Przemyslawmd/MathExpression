
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QVBoxLayout, QLabel, QWidget


class WindowAbout:

    def __init__(self):
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

        widget = QWidget()
        widget.setMinimumWidth(400)
        widget.setMinimumHeight(150)
        widget.setWindowModality(Qt.ApplicationModal)
        widget.setLayout(layout)
        widget.setGeometry(400, 400, 0, 0)
        widget.show()
        widget.exec_()


