
from collections import deque

from postfix.node import Node
from tokens.tokenGroup import TokenGroup


def create_tree(tokens):
    stack = deque()
    for token in tokens:
        if token.type in TokenGroup.operand:
            stack.append(token)
        elif token.type in TokenGroup.trigonometry:
            operand = stack.pop()
            left = operand if isinstance(operand, Node) else Node(operand)
            node = Node(token, left)
            stack.append(node)
        else:
            operand_1 = stack.pop()
            operand_2 = stack.pop()
            right = operand_1 if isinstance(operand_1, Node) else Node(operand_1)
            left = operand_2 if isinstance(operand_2, Node) else Node(operand_2)
            node = Node(token, left, right)
            stack.append(node)
    return stack.pop()

