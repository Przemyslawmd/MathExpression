from enum import Enum


class ErrorType(Enum):

    BRACKET = 0
    BRACKET_SQUARE = 1
    NEGATIVE_SYMBOL = 2
    SYMBOL = 3

    VALIDATOR_LOGARITHM = 4
    VALIDATOR_ROOT = 5


ErrorMessage = {
    ErrorType.BRACKET: "Improper bracket",
    ErrorType.BRACKET_SQUARE: "Improper square bracket",
    ErrorType.NEGATIVE_SYMBOL: "Improper usage of negative symbol",
    ErrorType.SYMBOL: "Improper symbol",
    ErrorType.VALIDATOR_LOGARITHM: "Symbols allowed to be followed by logarithm: x, number, opening bracket",
    ErrorType.VALIDATOR_ROOT: "Symbols allowed to be followed by sqrt: x, number, opening bracket",
}


