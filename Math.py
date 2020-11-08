
import sys

from PySide2.QtWidgets import (QApplication, QWidget)
from PySide2.QtWidgets import (QVBoxLayout, QHBoxLayout, QGridLayout)
from PySide2.QtWidgets import (QPushButton, QLineEdit, QTextEdit)
from PySide2.QtCore import Slot


class MathExpression(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        self.line_insert = QLineEdit()
        self.line_result = None
        self.create_gui()

    @Slot()
    def polish_notation(self):
        return

    @Slot()
    def reverse_polish_notation(self):
        return

    @Slot()
    def ast_tree(self):
        return

    @Slot()
    def input_token(self, token):
        self.line_insert.insert(token)

    @Slot()
    def remove_token(self):
        expression = self.line_insert.text()
        chars_to_remove = 1
        if expression.endswith('cos') or expression.endswith('sin') or expression.endswith('ctg'):
            chars_to_remove = 3
        elif expression.endswith('tg'):
            chars_to_remove = 2

        for i in range(chars_to_remove):
            self.line_insert.backspace()

    @Slot()
    def clear(self):
        self.line_insert.clear()

    def add_button(self, layout, func, width, label, row, column, column_span=1):
        button = QPushButton(label)
        button.setMaximumWidth(width)
        button.setMinimumWidth(width)
        button.clicked.connect(func)
        layout.addWidget(button, row, column, 1, column_span)

    def create_gui(self):
        self.line_result = QLineEdit()

        layout_control = QGridLayout()
        self.add_button(layout_control, lambda: self.input_token('0'), 50, '0', 0, 0)
        self.add_button(layout_control, lambda: self.input_token('1'), 50, '1', 0, 1)
        self.add_button(layout_control, lambda: self.input_token('2'), 50, '2', 0, 2)
        self.add_button(layout_control, lambda: self.input_token('3'), 50, '3', 0, 3)
        self.add_button(layout_control, lambda: self.input_token('4'), 50, '4', 0, 4)

        self.add_button(layout_control, lambda: self.input_token('('), 50, '(', 0, 5)
        self.add_button(layout_control, lambda: self.input_token(')'), 50, ')', 0, 6)
        self.add_button(layout_control, lambda: self.input_token('+'), 50, '+', 0, 7)
        self.add_button(layout_control, lambda: self.input_token('-'), 50, '-', 0, 8)
        self.add_button(layout_control, lambda: self.input_token('*'), 50, '*', 0, 9)
        self.add_button(layout_control, lambda: self.input_token('/'), 50, '/', 0, 10)

        self.add_button(layout_control, lambda: self.input_token('5'), 50, '5', 1, 0)
        self.add_button(layout_control, lambda: self.input_token('6'), 50, '6', 1, 1)
        self.add_button(layout_control, lambda: self.input_token('7'), 50, '7', 1, 2)
        self.add_button(layout_control, lambda: self.input_token('8'), 50, '8', 1, 3)
        self.add_button(layout_control, lambda: self.input_token('9'), 50, '9', 1, 4)

        self.add_button(layout_control, lambda: self.input_token('^'),      50, '^',      1, 5)
        self.add_button(layout_control, lambda: self.input_token("\u221A"), 50, "\u221A", 1, 6)
        self.add_button(layout_control, lambda: self.input_token('sin'),    50, 'sin',    1, 7)
        self.add_button(layout_control, lambda: self.input_token('cos'),    50, 'cos',    1, 8)
        self.add_button(layout_control, lambda: self.input_token('tg'),     50, 'tg',     1, 9)
        self.add_button(layout_control, lambda: self.input_token('ctg'),    50, 'ctg',    1, 10)

        self.add_button(layout_control, lambda: self.input_token('x'), 50,  'x',         2, 0)
        self.add_button(layout_control, lambda: self.remove_token(),   106, 'Backspace', 2, 1, 2)
        self.add_button(layout_control, lambda: self.clear(),          106, 'Clear',     2, 3, 2)

        layout_left = QVBoxLayout()
        layout_left.addWidget(self.line_insert)
        layout_left.addWidget(self.line_result)
        layout_left.addLayout(layout_control)

        button_polish = QPushButton("Polish Notation")
        button_polish.setMaximumWidth(220)
        button_reverse_polish = QPushButton("Reverse Polish Notation")
        button_reverse_polish.setMaximumWidth(220)
        button_ast_tree = QPushButton("AST Tree")
        button_ast_tree.setMaximumWidth(220)

        layout_right = QVBoxLayout()
        layout_right.addStretch()
        layout_right.addWidget(button_polish)
        layout_right.addWidget(button_reverse_polish)
        layout_right.addWidget(button_ast_tree)
        layout_right.addStretch()

        layout_main = QHBoxLayout()
        layout_main.addSpacing(10)
        layout_main.addLayout(layout_left, 68)
        layout_main.addSpacing(10)
        layout_main.addLayout(layout_right, 32)
        layout_main.addSpacing(10)
        self.setLayout(layout_main)

        return


if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = MathExpression()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec_())
