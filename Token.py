
from enum import Enum


class TokenValue(Enum):
    NONE = 0

    PLUS = 1
    MINUS = 2
    MULTIPLICATION = 3
    DIVISION = 4

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
    def __init__(self, token_value, token_number):

        if token_value != TokenValue.NONE and token_number != 0:
            raise Exception("For token value other than None token number should be zero")

        self.token_symbol = token_value
        self.token_number = token_number
        self.token_type = None
        self.set_token_type()

    def set_token_type(self):
        if self.token_symbol is TokenValue.NONE:
            self.token_type = TokenType.NUMBER
        elif self.token_symbol in (TokenValue.SINE, TokenValue.COSINE, TokenValue.TANGENT, TokenValue.COTANGENT):
            self.token_type = TokenType.TRIGONOMETRY
        elif self.token_symbol in (TokenValue.BRACKET_LEFT, TokenValue.BRACKET_RIGHT):
            self.token_type = TokenType.BRACKET
        else:
            self.token_type = TokenType.SYMBOL

