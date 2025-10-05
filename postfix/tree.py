
from collections import deque

from postfix.node import Node
from tokens.token import TokenType


one_operand = (TokenType.COSINE,
               TokenType.COTANGENT,
               TokenType.SINE,
               TokenType.TANGENT,
               TokenType.LOG)

def create_tree(tokens):
    stack = deque()
    for token in tokens:
        if token.type is TokenType.NUMBER or token.type is TokenType.X:
            stack.append(token)
        elif token.type in one_operand:
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

