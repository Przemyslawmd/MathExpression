
from Token.Token import Token, TokenType
from Errors import ErrorType, ErrorMessage
from Token.TokenUtils import TokenUtils


def add_multiplication_token(tokens):
    indices = []
    for index, token in enumerate(tokens[:-1]):
        if token.type in [TokenType.BRACKET_RIGHT, TokenType.X, TokenType.NUMBER]:
            next_token = tokens[index + 1]
            if next_token.type in [TokenType.SINE,
                                   TokenType.COSINE,
                                   TokenType.TANGENT,
                                   TokenType.COTANGENT,
                                   TokenType.X,
                                   TokenType.NUMBER,
                                   TokenType.BRACKET_LEFT,
                                   TokenType.ROOT,
                                   TokenType.LOG]:
                if token.type is TokenType.NUMBER and next_token.type is TokenType.NUMBER:
                    continue
                indices.append(index + 1)
    index_shift = 0
    for index in indices:
        tokens.insert(index + index_shift, Token(TokenType.MULTIPLICATION))
        index_shift += 1


def remove_angle_brackets(tokens):
    tokens_to_remove = []
    for index, token in enumerate(tokens):
        if token.type is not TokenType.BRACKET_ANGLE_LEFT:
            continue
        if index == 0:
            raise Exception(ErrorMessage[ErrorType.PARSER_BRACKET_ANGLE])
        if tokens[index - 1].type not in [TokenType.ROOT, TokenType.LOG]:
            raise Exception(ErrorMessage[ErrorType.PARSER_BRACKET_ANGLE])
        if tokens[index + 1].type is not TokenType.NUMBER:
            raise Exception(ErrorMessage[ErrorType.PARSER_BRACKET_ANGLE])
        if tokens[index + 2].type is not TokenType.BRACKET_ANGLE_RIGHT:
            raise Exception(ErrorMessage[ErrorType.PARSER_BRACKET_ANGLE])
        tokens[index - 1].data = tokens[index + 1].data
        tokens_to_remove.append(index)
        tokens_to_remove.append(index + 1)
        tokens_to_remove.append(index + 2)

    for i in range(len(tokens) - 1, -1, -1):
        if i in tokens_to_remove:
            del tokens[i]


def remove_negative_tokens(tokens):
    is_token_negative = False
    for index, token in enumerate(tokens):
        if token.type is TokenType.NEGATIVE:
            is_token_negative = True
            continue
        if is_token_negative:
            if token.type is TokenType.NUMBER:
                number = token.data
                tokens[index] = Token(TokenType.NUMBER, number * -1)
            elif token.type is TokenType.X:
                tokens[index] = Token(TokenType.X_NEGATIVE)
            elif token.type in [TokenType.BRACKET_LEFT, TokenType.ROOT, TokenType.LOG, TokenUtils.trigonometry]:
                tokens.insert(index, Token(TokenType.MULTIPLICATION))
                tokens.insert(index, Token(TokenType.NUMBER, -1))
            else:
                return False
            is_token_negative = False

    for i in range(len(tokens) - 1, -1, -1):
        if tokens[i].type is TokenType.NEGATIVE:
            del tokens[i]
    return True


def post_parse(tokens):
    remove_angle_brackets(tokens)
    add_multiplication_token(tokens)
    if not remove_negative_tokens(tokens):
        raise Exception(ErrorMessage[ErrorType.PARSER_NEGATIVE_SYMBOL])


