
from enum import Enum


class TokenType(Enum):

    NUMBER = 0

    PLUS = 1
    MINUS = 2
    MULTIPLICATION = 3
    DIVISION = 4

    SINE = 5
    COSINE = 6
    TANGENT = 7
    COTANGENT = 8

    LOG = 9
    NEGATIVE = 10
    POWER = 11
    ROOT = 12
    X = 13

    BRACKET_LEFT = 14
    BRACKET_RIGHT = 15
    BRACKET_ANGLE_LEFT = 16
    BRACKET_ANGLE_RIGHT = 17


class Token:
    def __init__(self, _type, data=0):
        self.type = _type
        self.data = data


