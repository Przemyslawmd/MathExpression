
from collections import deque

from tokens.token import Token, TokenType
from tokens.tokenGroup import TokenGroup

left_multiplication = (
    TokenType.BRACKET_RIGHT,
    TokenType.NUMBER,
    TokenType.X
)


right_multiplication = (
    TokenType.BRACKET_LEFT,
    TokenType.COSINE,
    TokenType.COTANGENT,
    TokenType.LOG,
    TokenType.NUMBER,
    TokenType.ROOT,
    TokenType.SINE,
    TokenType.TANGENT,
    TokenType.X
)


def add_multiplication_tokens(tokens):
    indices = []
    for index, token in enumerate(tokens[:-1]):
        if (token.type in left_multiplication
                and tokens[index + 1].type in right_multiplication
                and token.type is not tokens[index + 1].type):
            indices.append(index + 1)
    for index in reversed(indices):
        tokens.insert(index, Token(TokenType.MULTIPLICATION))


def remove_angle_brackets(tokens) -> bool:
    indices = []
    for index, token in enumerate(tokens):
        if token.type is not TokenType.BRACKET_ANGLE_LEFT:
            continue
        if index == 0:
            return False
        if tokens[index - 1].type not in (TokenType.ROOT, TokenType.LOG):
            return False
        if tokens[index + 1].type is not TokenType.NUMBER:
            return False
        if tokens[index + 2].type is not TokenType.BRACKET_ANGLE_RIGHT:
            return False
        tokens[index - 1].data = tokens[index + 1].data
        indices.extend([index, index + 1, index + 2])

    for index in reversed(indices):
        del tokens[index]
    return True


def remove_negative_tokens(tokens) -> bool:
    is_negative = False
    indices = deque()
    for index, token in enumerate(tokens):
        if token.type is TokenType.NEGATIVE:
            is_negative = True
            continue
        if is_negative:
            if token.type is TokenType.NUMBER:
                tokens[index].data *= -1
            elif token.type in (TokenType.BRACKET_LEFT, TokenType.ROOT, TokenType.LOG, TokenType.X, TokenGroup.trigonometry):
                indices.append(index)
            else:
                return False
            is_negative = False

    while indices:
        index = indices.pop()
        tokens.insert(index, Token(TokenType.MULTIPLICATION))
        tokens.insert(index, Token(TokenType.NUMBER, -1))

    for i in range(len(tokens) - 1, -1, -1):
        if tokens[i].type is TokenType.NEGATIVE:
            del tokens[i]
    return True

