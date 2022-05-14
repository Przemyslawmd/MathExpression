
from Tokens.Token import TokenType


class TokenUtils:

    bracket = [TokenType.BRACKET_LEFT, TokenType.BRACKET_RIGHT]

    basic_arithmetic = [TokenType.DIVISION, TokenType.MINUS, TokenType.MULTIPLICATION, TokenType.PLUS]

    trigonometry = [TokenType.COSINE, TokenType.COTANGENT, TokenType.SINE, TokenType.TANGENT]

    operators = basic_arithmetic + trigonometry + [TokenType.LOG, TokenType.POWER, TokenType.ROOT]


