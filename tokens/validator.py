
from errors import Error
from tokens.token import TokenType
from tokens.tokenGroup import TokenGroup


def validate_brackets(tokens) -> Error:
    round_counter = 0
    angle_counter = 0
    for token in tokens:
        if token.type is TokenType.BRACKET_LEFT:
            round_counter += 1
        elif token.type is TokenType.BRACKET_ANGLE_LEFT:
            angle_counter += 1
        elif token.type is TokenType.BRACKET_RIGHT:
            round_counter -= 1
            if round_counter < 0:
                return Error.PARSER_BRACKET
        elif token.type is TokenType.BRACKET_ANGLE_RIGHT:
            angle_counter -= 1
            if angle_counter < 0:
                return Error.PARSER_BRACKET_ANGLE

    if round_counter != 0:
        return Error.PARSER_BRACKET
    if angle_counter != 0:
        return Error.PARSER_BRACKET_ANGLE
    return Error.NO_ERROR


def validate_final(tokens) -> Error:
    last_index = len(tokens) - 1
    tokens_allowed = (TokenType.X, TokenType.NUMBER, TokenType.BRACKET_LEFT)
    tokens_forbidden = TokenGroup.basic_arithmetic + (TokenType.BRACKET_RIGHT,)
    for index, token in enumerate(tokens):
        if token.type is TokenType.LOG:
            if index == last_index or tokens[index + 1].type not in tokens_allowed:
                return Error.VALIDATOR_LOGARITHM
        if token.type is TokenType.POWER:
            if index == last_index or tokens[index + 1].type not in tokens_allowed:
                return Error.VALIDATOR_POWER
        if token.type is TokenType.ROOT:
            if index == last_index or tokens[index + 1].type not in tokens_allowed:
                return Error.VALIDATOR_ROOT
        if token.type in TokenGroup.trigonometry:
            if index == last_index or tokens[index + 1].type not in tokens_allowed:
                return Error.VALIDATOR_TRIGONOMETRY
        if token.type in TokenGroup.basic_arithmetic:
            if index == last_index or tokens[index + 1].type in tokens_forbidden:
                return Error.VALIDATOR_BASIC_ARITHMETIC
        if token.type is TokenType.NUMBER:
            if index != last_index and tokens[index + 1].type is TokenType.NUMBER:
                return Error.VALIDATOR_NUMBER
        return Error.NO_ERROR

