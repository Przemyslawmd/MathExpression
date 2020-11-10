
from enum import Enum


class TokenSymbol(Enum):
    NONE = 0
    PLUS = 1
    MINUS = 2
    MULTIPLICATION = 3
    DIVIDE = 4
    POWER = 5
    ROOT = 6
    LOG = 7

    SINE = 8
    COSINE = 9
    TANGENT = 10
    COTANGENT = 11

    BRACKET_LEFT = 12
    BRACKET_RIGHT = 13
    X = 14


class TokenType(Enum):
    NUMBER = 0
    SYMBOL = 1


class Token:
    def __init__(self, token_type, token_symbol, token_number):
        self.token_type = token_type
        self.token_symbol = token_symbol
        self.token_number = token_number

