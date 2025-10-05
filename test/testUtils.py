
from collections import namedtuple, deque
from math import isclose

TokenTest = namedtuple('TokenTest', 'type data', defaults=[0])


def check_tokens(tokens, tokens_test):
    assert len(tokens) == len(tokens_test)
    for token, token_test in zip(tokens, tokens_test):
        assert token.type == token_test.type
        if isinstance(token.data, float):
            assert isclose(token.data, token_test.data)
        else:
            assert token.data == token_test.data


def check_tree(root, tokens):
    assert root is not None
    tokens_stack = deque()
    for token in reversed(tokens):
        tokens_stack.append(token)
    traverse_tree(root, tokens_stack)


def traverse_tree(node, tokens):
    if node.left is not None:
        traverse_tree(node.left, tokens)
    if node.right is not None:
        traverse_tree(node.right, tokens)
    token = tokens.pop()
    assert node.token.type == token.type
    assert node.token.data == token.data

