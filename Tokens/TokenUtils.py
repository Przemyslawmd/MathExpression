
from Tokens.Token import TokenValue


class TokenUtils:

    @staticmethod
    def is_operation_token(token):
        return token.token_value in [TokenValue.DIVISION, TokenValue.MINUS, TokenValue.MULTIPLICATION, TokenValue.PLUS]


    @staticmethod
    def is_trigonometry_token(token):
        return token.token_value in [TokenValue.COSINE, TokenValue.COTANGENT, TokenValue.SINE, TokenValue.TANGENT]

