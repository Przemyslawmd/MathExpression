
from enum import Enum


class TokenSymbol(Enum):
    NONE = 0

    PLUS = 1
    MINUS = 2
    MULTIPLICATION = 3
    DIVIDE = 4

    SINE = 5
    COSINE = 6
    TANGENT = 7
    COTANGENT = 8

    POWER = 9
    ROOT = 10
    LOG = 11
    X = 12

    BRACKET_LEFT = 13
    BRACKET_RIGHT = 14


class TokenType(Enum):
    NUMBER = 0
    BRACKET = 1
    OPERATION = 2
    TRIGONOMETRY = 3
    SYMBOL = 4


class Token:
    def __init__(self, token_type, token_symbol, token_number):
        self.token_type = token_type
        self.token_symbol = token_symbol
        self.token_number = token_number
        self.validate()

    def validate(self):

        if self.token_type is TokenType.TRIGONOMETRY:
            if self.token_symbol not in (TokenSymbol.SINE, TokenSymbol.COSINE,
                                         TokenSymbol.TANGENT, TokenSymbol.COTANGENT):
                raise Exception("Improper value for trigonometry type")
            if self.token_number != 0:
                raise Exception("For trigonometry type token number should be zero")

        elif self.token_type is TokenType.NUMBER and self.token_symbol is not TokenSymbol.NONE:
            raise Exception("For number type TokenSymbol should be None")

        elif self.token_type is TokenType.BRACKET:
            if self.token_symbol not in (TokenSymbol.BRACKET_LEFT, TokenSymbol.BRACKET_RIGHT):
                raise Exception("Improper value for bracket type")
            if self.token_number != 0:
                raise Exception("For bracket type token number should be zero")

