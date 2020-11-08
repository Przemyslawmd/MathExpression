
from enum import Enum


class Token(Enum):
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9

    PLUS = 10
    MINUS = 11
    MULTIPLICATION = 12
    DIVIDE = 13
    POWER = 14
    ROOT = 15
    LOG = 16

    SINE = 17
    COSINE = 18
    TANGENT = 19
    COTANGENT = 20

    BRACKET_LEFT = 21
    BRACKET_RIGHT = 22
    X = 23
