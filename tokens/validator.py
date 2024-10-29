
from errors import Error
from tokens.token import TokenType
from tokens.tokenGroup import TokenGroup


allowed = {
    TokenType.BRACKET_RIGHT: (TokenType.BRACKET_RIGHT, TokenType.POWER) + TokenGroup.arithmetic,
    TokenType.NUMBER: (TokenType.X, TokenType.BRACKET_RIGHT, TokenType.POWER) + TokenGroup.arithmetic,
    TokenType.X: (TokenType.BRACKET_RIGHT, TokenGroup.arithmetic),
    TokenType.LOG: (TokenType.NUMBER, TokenType.X, TokenType.BRACKET_LEFT),
    TokenType.POWER: (TokenType.NUMBER, TokenType.X, TokenType.BRACKET_LEFT),
    TokenType.ROOT: (TokenType.NUMBER, TokenType.X, TokenType.BRACKET_LEFT),
    TokenGroup.trigonometry: (TokenType.NUMBER, TokenType.X, TokenType.BRACKET_LEFT)
}


forbidden = {
    TokenType.BRACKET_LEFT: (TokenType.BRACKET_RIGHT, TokenGroup.arithmetic),
    TokenGroup.arithmetic: (TokenType.BRACKET_RIGHT, TokenGroup.arithmetic)
}


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

    if tokens[0].type in (TokenType.BRACKET_RIGHT,
                          TokenType.PLUS,
                          TokenType.MINUS,
                          TokenType.DIVISION,
                          TokenType.POWER):
        return Error.VALIDATOR_FIRST_TOKEN

    last_index = len(tokens) - 1
    if tokens[last_index].type not in (TokenType.X,
                                       TokenType.NUMBER,
                                       TokenType.BRACKET_RIGHT):
        return Error.VALIDATOR_LAST_TOKEN

    for index, token in enumerate(tokens):
        if index == 0:
            continue
        if index == last_index:
            break

        next_type = tokens[index + 1].type
        match token.type:
            case TokenType.BRACKET_LEFT:
                if next_type in forbidden[TokenType.BRACKET_LEFT]:
                    return Error.VALIDATOR_BRACKET_LEFT
            case TokenType.BRACKET_RIGHT:
                if next_type not in allowed[TokenType.BRACKET_RIGHT]:
                    return Error.VALIDATOR_BRACKET_RIGHT
            case TokenType.LOG:
                if next_type not in allowed[TokenType.LOG]:
                    return Error.VALIDATOR_LOGARITHM
            case TokenType.POWER:
                if next_type not in allowed[TokenType.POWER]:
                    return Error.VALIDATOR_POWER
            case TokenType.ROOT:
                if next_type not in allowed[TokenType.ROOT]:
                    return Error.VALIDATOR_ROOT
            case TokenGroup.trigonometry:
                if next_type not in allowed[TokenGroup.trigonometry]:
                    return Error.VALIDATOR_TRIGONOMETRY
            case TokenGroup.arithmetic:
                if next_type in forbidden[TokenGroup.arithmetic]:
                    return Error.VALIDATOR_BASIC_ARITHMETIC
            case TokenType.NUMBER:
                if next_type not in allowed[TokenType.NUMBER]:
                    return Error.VALIDATOR_NUMBER
    return Error.NO_ERROR

