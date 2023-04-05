
import sys

from PySide6.QtWidgets import QApplication

from windowMain import MathExpression


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MathExpression()
    widget.create_gui()
    widget.resize(1400, 900)
    widget.show()
    sys.exit(app.exec())


