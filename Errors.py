from enum import Enum


class ErrorType(Enum):

    PARSER_BRACKET = 0
    PARSER_BRACKET_SQUARE = 1
    PARSER_NEGATIVE_SYMBOL = 2
    PARSER_SYMBOL = 3

    VALIDATOR_LOGARITHM = 4
    VALIDATOR_ROOT = 5
    VALIDATOR_TRIGONOMETRY = 6


ErrorMessage = {
    ErrorType.PARSER_BRACKET: "Improper bracket",
    ErrorType.PARSER_BRACKET_SQUARE: "Improper square bracket",
    ErrorType.PARSER_NEGATIVE_SYMBOL: "Improper usage of negative symbol",
    ErrorType.PARSER_SYMBOL: "Improper symbol",
    ErrorType.VALIDATOR_LOGARITHM: "Logarithm must be followed by: x, number, opening bracket",
    ErrorType.VALIDATOR_ROOT: "Root must be followed by: x, number, opening bracket",
    ErrorType.VALIDATOR_TRIGONOMETRY: "Trigomentry function must be be followed by: x, number, opening bracket",
}


