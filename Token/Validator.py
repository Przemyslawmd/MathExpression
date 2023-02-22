
from Token.Token import TokenType
from Token.TokenUtils import TokenUtils
from Errors import ErrorType, ErrorMessage


filter_positive = (TokenType.X, TokenType.NUMBER, TokenType.BRACKET_LEFT)
filter_negative = TokenUtils.basic_arithmetic + (TokenType.BRACKET_RIGHT,)


def validate(tokens):
    last = len(tokens) - 1
    for index, token in enumerate(tokens):
        if token.type is TokenType.LOG:
            if not tokens[index + 1] or tokens[index + 1].type not in filter_positive:
                raise Exception(ErrorMessage[ErrorType.VALIDATOR_LOGARITHM])
        if token.type is TokenType.POWER:
            if not tokens[index + 1] or tokens[index + 1].type not in filter_positive:
                raise Exception(ErrorMessage[ErrorType.VALIDATOR_POWER])
        if token.type is TokenType.ROOT:
            if not tokens[index + 1] or tokens[index + 1].type not in filter_positive:
                raise Exception(ErrorMessage[ErrorType.VALIDATOR_ROOT])
        if token.type in TokenUtils.trigonometry:
            if not tokens[index + 1] or tokens[index + 1].type not in filter_positive:
                raise Exception(ErrorMessage[ErrorType.VALIDATOR_TRIGONOMETRY])
        if token.type in TokenUtils.basic_arithmetic:
            if not tokens[index + 1] or tokens[index + 1].type in filter_negative:
                raise Exception(ErrorMessage[ErrorType.VALIDATOR_BASIC_ARITHMETIC])
        if token.type is TokenType.NUMBER:
            if index != last and tokens[index + 1].type is TokenType.NUMBER:
                raise Exception(ErrorMessage[ErrorType.VALIDATOR_NUMBER])


