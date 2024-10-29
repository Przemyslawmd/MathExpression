from enum import Enum


class Error(Enum):
    NO_ERROR = 0

    MAX_POINTS = 1

    PARSER_BRACKET = 2
    PARSER_BRACKET_ANGLE = 3
    PARSER_NEGATIVE_SYMBOL = 4
    PARSER_SYMBOL = 5

    VALIDATOR_BASIC_ARITHMETIC = 6
    VALIDATOR_FIRST_TOKEN = 7
    VALIDATOR_LAST_TOKEN = 8
    VALIDATOR_LOGARITHM = 9
    VALIDATOR_NUMBER = 10
    VALIDATOR_POWER = 11
    VALIDATOR_ROOT = 12
    VALIDATOR_TRIGONOMETRY = 13


ErrorMessage = {
    Error.MAX_POINTS: "Number of maximum points (100000) to calculate is exceeded, change x range or precision.",
    Error.PARSER_BRACKET: "Improper bracket.",
    Error.PARSER_BRACKET_ANGLE: "Improper angle bracket. Angle brackets are allowed only as a base for logarithm "
                                "and root.",
    Error.PARSER_NEGATIVE_SYMBOL: "Improper usage of negative symbol.",
    Error.PARSER_SYMBOL: "Improper symbol.",
    Error.VALIDATOR_NUMBER: "Empty space between numbers.",
    Error.VALIDATOR_BASIC_ARITHMETIC: "Addition, subtraction, multiplication, and division can not be followed"
                                      " by the same symbol and right bracket.",
    Error.VALIDATOR_LOGARITHM: "Logarithm can be followed only by : x, number, opening bracket.",
    Error.VALIDATOR_POWER: "Power can be followed only by : x, number, opening bracket.",
    Error.VALIDATOR_ROOT: "Root can be followed only by : x, number, opening bracket.",
    Error.VALIDATOR_TRIGONOMETRY: "Trigonometry function can be be followed only by : x, number, opening bracket.",
}
