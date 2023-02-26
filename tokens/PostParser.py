
from Errors import ErrorType, ErrorMessage
from tokens.Token import Token, TokenType
from tokens.TokenUtils import TokenUtils

left_multiplication_tokens = (
    TokenType.BRACKET_RIGHT,
    TokenType.NUMBER,
    TokenType.X
)


right_multiplication_tokens = (
    TokenType.BRACKET_LEFT,
    TokenType.COSINE,
    TokenType.COTANGENT,
    TokenType.LOG,
    TokenType.NUMBER,
    TokenType.ROOT,
    TokenType.SINE,
    TokenType.TANGENT,
    TokenType.X
)


def add_multiplication_tokens(tokens):
    indices_to_add_multiplication = []
    for index, token in enumerate(tokens[:-1]):
        if token.type in left_multiplication_tokens:
            if tokens[index + 1].type in right_multiplication_tokens:
                indices_to_add_multiplication.append(index + 1)
    index_shift = 0
    for index in indices_to_add_multiplication:
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
        tokens_to_remove.extend([index, index + 1, index + 2])

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
    add_multiplication_tokens(tokens)
    if not remove_negative_tokens(tokens):
        raise Exception(ErrorMessage[ErrorType.PARSER_NEGATIVE_SYMBOL])


