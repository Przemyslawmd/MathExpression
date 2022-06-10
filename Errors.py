from enum import Enum


class ErrorType(Enum):

    MAX_POINTS = 0

    PARSER_BRACKET = 1
    PARSER_BRACKET_ANGLE = 2
    PARSER_NEGATIVE_SYMBOL = 3
    PARSER_SYMBOL = 4

    VALIDATOR_BASIC_ARITHMETIC = 5
    VALIDATOR_LOGARITHM = 6
    VALIDATOR_NUMBER = 7
    VALIDATOR_POWER = 8
    VALIDATOR_ROOT = 9
    VALIDATOR_TRIGONOMETRY = 10


ErrorMessage = {
    ErrorType.MAX_POINTS: "Number of maximum points (100000) to calculate is exceeded, change x range or precision.",
    ErrorType.PARSER_BRACKET: "Improper bracket.",
    ErrorType.PARSER_BRACKET_ANGLE: "Improper angle bracket. Angle brackets are allowed only as a base for logarithm "
                                    "and root.",
    ErrorType.PARSER_NEGATIVE_SYMBOL: "Improper usage of negative symbol.",
    ErrorType.PARSER_SYMBOL: "Improper symbol.",
    ErrorType.VALIDATOR_NUMBER: "Empty space between numbers.",
    ErrorType.VALIDATOR_BASIC_ARITHMETIC: "Addition, subtraction, multiplication, and division can not be followed"
                                          " by the same symbol and right bracket.",
    ErrorType.VALIDATOR_LOGARITHM: "Logarithm can be followed only by : x, number, opening bracket.",
    ErrorType.VALIDATOR_POWER: "Power can be followed only by : x, number, opening bracket.",
    ErrorType.VALIDATOR_ROOT: "Root can be followed only by : x, number, opening bracket.",
    ErrorType.VALIDATOR_TRIGONOMETRY: "Trigonometry function can be be followed only by : x, number, opening bracket.",
}


