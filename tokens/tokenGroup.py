
from tokens.token import TokenType


class TokenGroup:

    arithmetic = (TokenType.DIVISION, TokenType.MINUS, TokenType.MULTIPLICATION, TokenType.PLUS)

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

