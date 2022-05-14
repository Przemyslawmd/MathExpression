from enum import Enum


class ErrorType(Enum):

    PARSER_BRACKET = 0
    PARSER_BRACKET_SQUARE = 1
    PARSER_NEGATIVE_SYMBOL = 2
    PARSER_SYMBOL = 3

    VALIDATOR_BASIC_ARITHMETIC = 4
    VALIDATOR_LOGARITHM = 5
    VALIDATOR_POWER = 6
    VALIDATOR_ROOT = 7
    VALIDATOR_TRIGONOMETRY = 8


ErrorMessage = {
    ErrorType.PARSER_BRACKET: "Improper bracket",
    ErrorType.PARSER_BRACKET_SQUARE: "Improper square bracket",
    ErrorType.PARSER_NEGATIVE_SYMBOL: "Improper usage of negative symbol",
    ErrorType.PARSER_SYMBOL: "Improper symbol",
    ErrorType.VALIDATOR_BASIC_ARITHMETIC: "Addition, substraction, multiplication, and division can not be followed"
                                          " by the same symbol and right bracket",
    ErrorType.VALIDATOR_LOGARITHM: "Logarithm can be followed only by : x, number, opening bracket",
    ErrorType.VALIDATOR_POWER: "Power can be followed only by : x, number, opening bracket",
    ErrorType.VALIDATOR_ROOT: "Root can be followed only by : x, number, opening bracket",
    ErrorType.VALIDATOR_TRIGONOMETRY: "Trigomentry function can be be followed only by : x, number, opening bracket",
}


