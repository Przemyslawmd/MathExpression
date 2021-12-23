
from enum import Enum


class TokenValue(Enum):

    # Token of type NUMBER
    NUMBER = 0

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


class Token:
    def __init__(self, value, token_number=0):

        if value != TokenValue.NUMBER and token_number != 0:
            raise Exception("For token value other than Number token number should be zero")

        self.value = value
        self.number = token_number


