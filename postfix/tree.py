
from collections import deque

from postfix.node import Node
from tokens.token import TokenType


def create_tree(tokens):
    stack = deque()
    for token in tokens:
        if token.type is TokenType.NUMBER or token.type is TokenType.X:
            stack.append(token)
        else:
            token_1 = stack.pop()
            token_2 = stack.pop()
            right = token_1 if isinstance(token_1, Node) else Node(token_1)
            left = token_2 if isinstance(token_2, Node) else Node(token_2)
            node = Node(token, left, right)
            stack.append(node)
    return stack.pop()

