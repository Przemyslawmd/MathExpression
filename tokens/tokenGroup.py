
from tokens.token import TokenType


class TokenGroup:

    bracket = (TokenType.BRACKET_LEFT, TokenType.BRACKET_RIGHT)

    basic_arithmetic = (TokenType.DIVISION, TokenType.MINUS, TokenType.MULTIPLICATION, TokenType.PLUS)

    two_operands = (TokenType.DIVISION,
                    TokenType.MINUS,
                    TokenType.MULTIPLICATION,
                    TokenType.PLUS,
                    TokenType.POWER)

    trigonometry = (TokenType.COSINE, TokenType.COTANGENT, TokenType.SINE, TokenType.TANGENT)

    operators = (TokenType.DIVISION,
                 TokenType.MINUS,
                 TokenType.MULTIPLICATION,
                 TokenType.PLUS,
                 TokenType.COSINE,
                 TokenType.COTANGENT,
                 TokenType.SINE,
                 TokenType.TANGENT,
                 TokenType.LOG,
                 TokenType.POWER,
                 TokenType.ROOT)


