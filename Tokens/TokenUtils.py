
from Tokens.Token import TokenValue


class TokenUtils:

    bracket = [TokenValue.BRACKET_LEFT, TokenValue.BRACKET_RIGHT]

    operation = [TokenValue.DIVISION, TokenValue.MINUS, TokenValue.MULTIPLICATION, TokenValue.PLUS]

    trigonometry = [TokenValue.COSINE, TokenValue.COTANGENT, TokenValue.SINE, TokenValue.TANGENT]

    operators = operation + trigonometry + [TokenValue.LOG, TokenValue.POWER, TokenValue.ROOT]


