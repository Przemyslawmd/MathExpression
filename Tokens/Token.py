
from enum import Enum


class TokenValue(Enum):

    # Token of type NUMBER
    NONE = 0

    # Tokens of type OPERATION
    PLUS = 1
    MINUS = 2
    MULTIPLICATION = 3
    DIVISION = 4

    # Tokens of type TRIGONOMETRY
    SINE = 5
    COSINE = 6
    TANGENT = 7
    COTANGENT = 8

    # Tokens of type OTHER
    LOG = 9
    NEGATIVE = 10
    POWER = 11
    ROOT = 12
    X = 13
    X_NEGATIVE = 14

    # Tokens of type BRACKET
    BRACKET_LEFT = 15
    BRACKET_RIGHT = 16



class TokenType(Enum):
    NUMBER = 0
    BRACKET = 1
    OPERATION = 2
    TRIGONOMETRY = 3
    OTHER = 4


class Token:
    def __init__(self, token_value, token_number):

        if token_value != TokenValue.NONE and token_number != 0:
            raise Exception("For token value other than None token number should be zero")

        self.token_value = token_value
        self.token_number = token_number
        self.token_type = None
        self.set_token_type()

    def set_token_type(self):
        if self.token_value is TokenValue.NONE:
            self.token_type = TokenType.NUMBER
        elif self.token_value in (TokenValue.SINE, TokenValue.COSINE, TokenValue.TANGENT, TokenValue.COTANGENT):
            self.token_type = TokenType.TRIGONOMETRY
        elif self.token_value in (TokenValue.PLUS, TokenValue.MINUS, TokenValue.MULTIPLICATION, TokenValue.DIVISION):
            self.token_type = TokenType.OPERATION
        elif self.token_value in (TokenValue.BRACKET_LEFT, TokenValue.BRACKET_RIGHT):
            self.token_type = TokenType.BRACKET
        else:
            self.token_type = TokenType.OTHER

