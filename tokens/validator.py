
from errors import Error, ErrorMessage
from tokens.token import TokenType
from tokens.tokenGroup import TokenGroup


def validate_brackets(tokens):
    round_validator = 0
    angle_validator = 0
    for token in tokens:
        if token.type is TokenType.BRACKET_LEFT:
            round_validator += 1
        elif token.type is TokenType.BRACKET_RIGHT:
            if round_validator == 0:
                raise Exception(ErrorMessage[Error.PARSER_BRACKET])
            round_validator -= 1
        elif token.type is TokenType.BRACKET_ANGLE_LEFT:
            angle_validator += 1
        elif token.type is TokenType.BRACKET_ANGLE_RIGHT:
            if angle_validator == 0:
                raise Exception(ErrorMessage[Error.PARSER_BRACKET_ANGLE])
            angle_validator -= 1

    if round_validator != 0:
        raise Exception(ErrorMessage[Error.PARSER_BRACKET])
    if angle_validator != 0:
        raise Exception(ErrorMessage[Error.PARSER_BRACKET_ANGLE])


def validate_final(tokens):
    last_index = len(tokens) - 1
    tokens_allowed = (TokenType.X, TokenType.NUMBER, TokenType.BRACKET_LEFT)
    tokens_forbidden = TokenGroup.basic_arithmetic + (TokenType.BRACKET_RIGHT,)
    for index, token in enumerate(tokens):
        if token.type is TokenType.LOG:
            if index == last_index or tokens[index + 1].type not in tokens_allowed:
                raise Exception(ErrorMessage[Error.VALIDATOR_LOGARITHM])
        if token.type is TokenType.POWER:
            if index == last_index or tokens[index + 1].type not in tokens_allowed:
                raise Exception(ErrorMessage[Error.VALIDATOR_POWER])
        if token.type is TokenType.ROOT:
            if index == last_index or tokens[index + 1].type not in tokens_allowed:
                raise Exception(ErrorMessage[Error.VALIDATOR_ROOT])
        if token.type in TokenGroup.trigonometry:
            if index == last_index or tokens[index + 1].type not in tokens_allowed:
                raise Exception(ErrorMessage[Error.VALIDATOR_TRIGONOMETRY])
        if token.type in TokenGroup.basic_arithmetic:
            if index == last_index or tokens[index + 1].type in tokens_forbidden:
                raise Exception(ErrorMessage[Error.VALIDATOR_BASIC_ARITHMETIC])
        if token.type is TokenType.NUMBER:
            if index != last_index and tokens[index + 1].type is TokenType.NUMBER:
                raise Exception(ErrorMessage[Error.VALIDATOR_NUMBER])


