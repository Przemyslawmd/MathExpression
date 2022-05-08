from enum import Enum


class ErrorType(Enum):

    BRACKET = 0
    BRACKET_SQUARE = 1
    NEGATIVE_SYMBOL = 2
    SYMBOL = 3


ErrorMessage = {
    ErrorType.BRACKET: "Improper bracket",
    ErrorType.BRACKET_SQUARE: "Improper square bracket",
    ErrorType.NEGATIVE_SYMBOL: "Improper usage of negative symbol",
    ErrorType.SYMBOL: "Improper symbol",
}


