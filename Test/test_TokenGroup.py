
from unittest import TestCase
from Tokens.Parser import Parser
from Tokens.Token import TokenType, TokenValue
from Tokens.TokenGroup import TokenGroup


class TestTokenGroup(TestCase):

    @staticmethod
    def check_token(token, token_type, token_number, token_value):
        assert token.token_type is token_type
        assert token.token_number == token_number
        assert token.token_value is token_value


    def test_group_tokens_1(self):
        tokens = Parser("2x^3 + log10").parse()
        tokens_grouped = TokenGroup().create_tokens(tokens)
        assert len(tokens_grouped) is 3
        assert len(tokens_grouped[0]) is 4
        assert len(tokens_grouped[1]) is 1
        assert len(tokens_grouped[2]) is 2
        self.check_token(tokens_grouped[0][1], TokenType.OTHER, 0, TokenValue.X)
        self.check_token(tokens_grouped[0][3], TokenType.NUMBER, 3, TokenValue.NUMBER)


    def test_group_tokens_2(self):
        tokens = Parser("(6x +3)(2sinx+4)").parse()
        tokens_grouped = TokenGroup().create_tokens(tokens)
        assert len(tokens_grouped) is 11
        assert len(tokens_grouped[0]) is 1
        assert len(tokens_grouped[1]) is 2
        assert len(tokens_grouped[2]) is 1
        assert len(tokens_grouped[3]) is 1
        assert len(tokens_grouped[4]) is 1
        assert len(tokens_grouped[5]) is 1
        assert len(tokens_grouped[6]) is 1
        assert len(tokens_grouped[7]) is 3
        assert len(tokens_grouped[8]) is 1
        assert len(tokens_grouped[9]) is 1
        assert len(tokens_grouped[10]) is 1
        self.check_token(tokens_grouped[1][0], TokenType.NUMBER, 6, TokenValue.NUMBER)
        self.check_token(tokens_grouped[1][1], TokenType.OTHER,  0, TokenValue.X)
        self.check_token(tokens_grouped[9][0], TokenType.NUMBER, 4, TokenValue.NUMBER)


    def test_group_tokens_3(self):
        tokens = Parser("2(3x +  cosx)(7  + x^3 )").parse()
        tokens_grouped = TokenGroup().create_tokens(tokens)
        assert len(tokens_grouped) is 13
        assert len(tokens_grouped[0]) is 1
        assert len(tokens_grouped[1]) is 1
        assert len(tokens_grouped[2]) is 1
        assert len(tokens_grouped[3]) is 2
        assert len(tokens_grouped[4]) is 1
        assert len(tokens_grouped[5]) is 2
        assert len(tokens_grouped[6]) is 1
        assert len(tokens_grouped[7]) is 1
        assert len(tokens_grouped[8]) is 1
        assert len(tokens_grouped[9]) is 1
        assert len(tokens_grouped[10]) is 1
        assert len(tokens_grouped[11]) is 3
        assert len(tokens_grouped[12]) is 1
        self.check_token(tokens_grouped[0][0], TokenType.NUMBER, 2, TokenValue.NUMBER)
        self.check_token(tokens_grouped[3][1],  TokenType.OTHER,     0, TokenValue.X)
        self.check_token(tokens_grouped[10][0], TokenType.OPERATION, 0, TokenValue.PLUS)
        self.check_token(tokens_grouped[11][1], TokenType.OTHER,     0, TokenValue.POWER)


    def test_group_tokens_4(self):
        tokens = Parser("10(logsinx^4 + 17x)").parse()
        tokens_grouped = TokenGroup().create_tokens(tokens)
        assert len(tokens_grouped) is 7
        assert len(tokens_grouped[0]) is 1
        assert len(tokens_grouped[1]) is 1
        assert len(tokens_grouped[2]) is 1
        assert len(tokens_grouped[3]) is 5
        assert len(tokens_grouped[4]) is 1
        assert len(tokens_grouped[5]) is 2
        assert len(tokens_grouped[6]) is 1
        self.check_token(tokens_grouped[0][0], TokenType.NUMBER, 10, TokenValue.NUMBER)
        self.check_token(tokens_grouped[3][0], TokenType.OTHER,   0, TokenValue.LOG)
        self.check_token(tokens_grouped[3][3], TokenType.OTHER,   0, TokenValue.POWER)
        self.check_token(tokens_grouped[3][4], TokenType.NUMBER, 4, TokenValue.NUMBER)
        self.check_token(tokens_grouped[6][0], TokenType.BRACKET, 0, TokenValue.BRACKET_RIGHT)


