
from Errors import Error, ErrorMessage
from tokens.token import TokenType
from tokens.utils import TokenUtils


def validate_brackets(tokens):
    round_brackets_validator = 0
    angle_brackets_validator = 0
    for token in tokens:
        if token.type is TokenType.BRACKET_LEFT:
            round_brackets_validator += 1
        elif token.type is TokenType.BRACKET_RIGHT:
            if round_brackets_validator == 0:
                raise Exception(ErrorMessage[Error.PARSER_BRACKET])
            round_brackets_validator -= 1
        elif token.type is TokenType.BRACKET_ANGLE_LEFT:
            angle_brackets_validator += 1
        elif token.type is TokenType.BRACKET_ANGLE_RIGHT:
            if angle_brackets_validator == 0:
                raise Exception(ErrorMessage[Error.PARSER_BRACKET_ANGLE])
            angle_brackets_validator -= 1

    if round_brackets_validator != 0:
        raise Exception(ErrorMessage[Error.PARSER_BRACKET])
    if angle_brackets_validator != 0:
        raise Exception(ErrorMessage[Error.PARSER_BRACKET_ANGLE])


def validate_final(tokens):
    last = len(tokens) - 1
    filter_positive = (TokenType.X, TokenType.NUMBER, TokenType.BRACKET_LEFT)
    filter_negative = TokenUtils.basic_arithmetic + (TokenType.BRACKET_RIGHT,)
    for index, token in enumerate(tokens):
        if token.type is TokenType.LOG:
            if not tokens[index + 1] or tokens[index + 1].type not in filter_positive:
                raise Exception(ErrorMessage[Error.VALIDATOR_LOGARITHM])
        if token.type is TokenType.POWER:
            if not tokens[index + 1] or tokens[index + 1].type not in filter_positive:
                raise Exception(ErrorMessage[Error.VALIDATOR_POWER])
        if token.type is TokenType.ROOT:
            if not tokens[index + 1] or tokens[index + 1].type not in filter_positive:
                raise Exception(ErrorMessage[Error.VALIDATOR_ROOT])
        if token.type in TokenUtils.trigonometry:
            if not tokens[index + 1] or tokens[index + 1].type not in filter_positive:
                raise Exception(ErrorMessage[Error.VALIDATOR_TRIGONOMETRY])
        if token.type in TokenUtils.basic_arithmetic:
            if not tokens[index + 1] or tokens[index + 1].type in filter_negative:
                raise Exception(ErrorMessage[Error.VALIDATOR_BASIC_ARITHMETIC])
        if token.type is TokenType.NUMBER:
            if index != last and tokens[index + 1].type is TokenType.NUMBER:
                raise Exception(ErrorMessage[Error.VALIDATOR_NUMBER])


