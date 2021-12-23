
from Tokens.Token import TokenValue


class TokenUtils:

    operation = [TokenValue.DIVISION, TokenValue.MINUS, TokenValue.MULTIPLICATION, TokenValue.PLUS]

    trigonometry = [TokenValue.COSINE, TokenValue.COTANGENT, TokenValue.SINE, TokenValue.TANGENT]


    @staticmethod
    def append_operation(token_values):
        for token_value in TokenUtils.operation:
            token_values.append(token_value)


    @staticmethod
    def append_trigonometry(token_values):
        for token_value in TokenUtils.trigonometry:
            token_values.append(token_value)


