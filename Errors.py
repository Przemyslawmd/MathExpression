from enum import Enum


class ErrorType(Enum):

    PARSER_BRACKET = 0
    PARSER_BRACKET_SQUARE = 1
    PARSER_NEGATIVE_SYMBOL = 2
    PARSER_SYMBOL = 3

    VALIDATOR_LOGARITHM = 4
    VALIDATOR_ROOT = 5


ErrorMessage = {
    ErrorType.PARSER_BRACKET: "Improper bracket",
    ErrorType.PARSER_BRACKET_SQUARE: "Improper square bracket",
    ErrorType.PARSER_NEGATIVE_SYMBOL: "Improper usage of negative symbol",
    ErrorType.PARSER_SYMBOL: "Improper symbol",
    ErrorType.VALIDATOR_LOGARITHM: "Symbols allowed to be followed by logarithm: x, number, opening bracket",
    ErrorType.VALIDATOR_ROOT: "Symbols allowed to be followed by sqrt: x, number, opening bracket",
}


