
from Tokens.Token import TokenValue


class TokenUtils:

    bracket = [TokenValue.BRACKET_LEFT, TokenValue.BRACKET_RIGHT]

    basic_arithmetic = [TokenValue.DIVISION, TokenValue.MINUS, TokenValue.MULTIPLICATION, TokenValue.PLUS]

    trigonometry = [TokenValue.COSINE, TokenValue.COTANGENT, TokenValue.SINE, TokenValue.TANGENT]

    operators = basic_arithmetic + trigonometry + [TokenValue.LOG, TokenValue.POWER, TokenValue.ROOT]


