
from Tokens.Token import TokenValue


class TokenUtils:

    bracket = [TokenValue.BRACKET_LEFT, TokenValue.BRACKET_RIGHT]

    operation = [TokenValue.DIVISION, TokenValue.MINUS, TokenValue.MULTIPLICATION, TokenValue.PLUS]

    trigonometry = [TokenValue.COSINE, TokenValue.COTANGENT, TokenValue.SINE, TokenValue.TANGENT]

    operators = operation + trigonometry + [TokenValue.LOG, TokenValue.POWER, TokenValue.ROOT]


    @staticmethod
    def append_operation(token_values):
        for token_value in TokenUtils.operation:
            token_values.append(token_value)


    @staticmethod
    def append_trigonometry(token_values):
        for token_value in TokenUtils.trigonometry:
            token_values.append(token_value)


