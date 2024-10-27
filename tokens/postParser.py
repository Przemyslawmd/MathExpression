
from tokens.token import Token, TokenType
from tokens.tokenGroup import TokenGroup

left_multiplication = (
    TokenType.BRACKET_RIGHT,
    TokenType.NUMBER,
    TokenType.X
)


right_multiplication = (
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
        if token.type in left_multiplication:
            if tokens[index + 1].type in right_multiplication:
                indices_to_add_multiplication.append(index + 1)
    index_shift = 0
    for index in indices_to_add_multiplication:
        tokens.insert(index + index_shift, Token(TokenType.MULTIPLICATION))
        index_shift += 1


def remove_angle_brackets(tokens) -> bool:
    tokens_to_remove = []
    for index, token in enumerate(tokens):
        if token.type is not TokenType.BRACKET_ANGLE_LEFT:
            continue
        if index == 0:
            return False
        if tokens[index - 1].type not in [TokenType.ROOT, TokenType.LOG]:
            return False
        if tokens[index + 1].type is not TokenType.NUMBER:
            return False
        if tokens[index + 2].type is not TokenType.BRACKET_ANGLE_RIGHT:
            return False
        tokens[index - 1].data = tokens[index + 1].data
        tokens_to_remove.extend([index, index + 1, index + 2])

    for i in range(len(tokens) - 1, -1, -1):
        if i in tokens_to_remove:
            del tokens[i]
    return True


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
            elif token.type in [TokenType.BRACKET_LEFT, TokenType.ROOT, TokenType.LOG, TokenGroup.trigonometry]:
                tokens.insert(index, Token(TokenType.MULTIPLICATION))
                tokens.insert(index, Token(TokenType.NUMBER, -1))
            else:
                return False
            is_token_negative = False

    for i in range(len(tokens) - 1, -1, -1):
        if tokens[i].type is TokenType.NEGATIVE:
            del tokens[i]
    return True

