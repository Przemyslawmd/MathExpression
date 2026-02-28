
from enum import Enum


class Error(Enum):
    NO_ERROR = 0

    MAX_POINTS = 1

    PARSER_BRACKET = 2
    PARSER_BRACKET_ANGLE = 3
    PARSER_NEGATIVE_SYMBOL = 4
    PARSER_SYMBOL = 5

    VALIDATOR_ARITHMETIC = 6
    VALIDATOR_BRACKET_LEFT = 7
    VALIDATOR_BRACKET_RIGHT = 8
    VALIDATOR_FIRST_TOKEN = 9
    VALIDATOR_LAST_TOKEN = 10
    VALIDATOR_LOGARITHM = 11
    VALIDATOR_LOGARITHM_BASE = 12
    VALIDATOR_NUMBER = 13
    VALIDATOR_POWER = 14
    VALIDATOR_ROOT = 15
    VALIDATOR_ROOT_DEGREE = 16
    VALIDATOR_TRIGONOMETRY = 17
    VALIDATOR_X = 18

    INTERNAL_EXCEPTION_SINGLE_TOKEN = 19


Message = {
    Error.MAX_POINTS:
        "Number of maximum points (1 000 000) is exceeded, change x range or precision.",
    Error.PARSER_BRACKET:
        "Parsing brackets error.",
    Error.PARSER_BRACKET_ANGLE:
        "Invalid angle bracket\nAngle brackets can be used only as a base for logarithm or a degree for root, "
        "pattern is sqrt<NUMBER> or log<NUMBER>\nFor example: sqrt<4>16, log<2>x",
    Error.PARSER_NEGATIVE_SYMBOL:
        "Improper usage of the negative symbol",
    Error.PARSER_SYMBOL:
        "Invalid symbol",
    Error.VALIDATOR_BRACKET_LEFT:
        "Invalid symbol after the left bracket: plus, multiplication, division and the closing bracket are prohibited",
    Error.VALIDATOR_BRACKET_RIGHT:
        "Improper symbol after the right bracket",
    Error.VALIDATOR_FIRST_TOKEN:
        "Invalid the first symbol in the expression",
    Error.VALIDATOR_LAST_TOKEN:
        "Invalid the last symbol in the expression",
    Error.VALIDATOR_NUMBER:
        "Empty space between numbers",
    Error.VALIDATOR_ARITHMETIC:
        "Invalid symbol after the basic arithmetic symbol: plus, multiplication, division and the closing bracket are prohibited",
    Error.VALIDATOR_LOGARITHM:
        "Logarithm can be followed only by : x, number and the opening bracket",
    Error.VALIDATOR_LOGARITHM_BASE:
        "The base of the logarithm must be a positive number and different from 1",
    Error.VALIDATOR_POWER:
        "Power can be followed only by : x, number and the opening bracket",
    Error.VALIDATOR_ROOT:
        "Root can be followed only by : x, number and the opening bracket",
    Error.VALIDATOR_ROOT_DEGREE:
        "Zero is not allowed as a root degree",
    Error.VALIDATOR_TRIGONOMETRY:
        "Trigonometry function can be be followed only by : x, number, opening bracket",
    Error.VALIDATOR_X:
        "Invalid symbol after X, symbols allowed: right bracket, plus, minus, division and multiplication",
    Error.INTERNAL_EXCEPTION_SINGLE_TOKEN:
        "Exception: Single token is not X and not number",
}

