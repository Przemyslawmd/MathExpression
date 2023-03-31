
from collections import namedtuple

from unittest import TestCase

from tokens.parser import Parser
from tokens.token import TokenType


TokenTest = namedtuple('TokenTest', 'type data', defaults=[0])


class TestParser(TestCase):

    @staticmethod
    def check_token(token, token_data, token_value):
        assert token.data == token_data
        assert token.type is token_value

    @staticmethod
    def check_tokens(tokens, tokens_test):
        assert len(tokens) == len(tokens_test)
        for token, token_test in zip(tokens, tokens_test):
            assert token.type == token_test.type
            assert token.data == token_test.data


    def test_basic_1(self):
        tokens = Parser("2x + 3").parse()
        tokens_test = [TokenTest(TokenType.NUMBER, 2),
                       TokenTest(TokenType.MULTIPLICATION),
                       TokenTest(TokenType.X),
                       TokenTest(TokenType.PLUS),
                       TokenTest(TokenType.NUMBER, 3)]
        self.check_tokens(tokens, tokens_test)


    def test_basic_2(self):
        tokens = Parser("3(4x + cos30)").parse()
        tokens_test = [TokenTest(TokenType.NUMBER, 3),
                       TokenTest(TokenType.MULTIPLICATION),
                       TokenTest(TokenType.BRACKET_LEFT),
                       TokenTest(TokenType.NUMBER, 4),
                       TokenTest(TokenType.MULTIPLICATION),
                       TokenTest(TokenType.X),
                       TokenTest(TokenType.PLUS),
                       TokenTest(TokenType.COSINE),
                       TokenTest(TokenType.NUMBER, 30),
                       TokenTest(TokenType.BRACKET_RIGHT)]
        self.check_tokens(tokens, tokens_test)


    def test_basic_3(self):
        tokens = Parser("3(4x + 12cos30)").parse()
        tokens_test = [TokenTest(TokenType.NUMBER, 3),
                       TokenTest(TokenType.MULTIPLICATION),
                       TokenTest(TokenType.BRACKET_LEFT),
                       TokenTest(TokenType.NUMBER, 4),
                       TokenTest(TokenType.MULTIPLICATION),
                       TokenTest(TokenType.X),
                       TokenTest(TokenType.PLUS),
                       TokenTest(TokenType.NUMBER, 12),
                       TokenTest(TokenType.MULTIPLICATION),
                       TokenTest(TokenType.COSINE),
                       TokenTest(TokenType.NUMBER, 30),
                       TokenTest(TokenType.BRACKET_RIGHT)]
        self.check_tokens(tokens, tokens_test)


    def test_basic_4(self):
        tokens = Parser("(4 + x)sinx").parse()
        tokens_test = [TokenTest(TokenType.BRACKET_LEFT),
                       TokenTest(TokenType.NUMBER, 4),
                       TokenTest(TokenType.PLUS),
                       TokenTest(TokenType.X),
                       TokenTest(TokenType.BRACKET_RIGHT),
                       TokenTest(TokenType.MULTIPLICATION),
                       TokenTest(TokenType.SINE),
                       TokenTest(TokenType.X)]
        self.check_tokens(tokens, tokens_test)


    def test_basic_5(self):
        tokens = Parser("xtg12").parse()
        tokens_test = [TokenTest(TokenType.X),
                       TokenTest(TokenType.MULTIPLICATION),
                       TokenTest(TokenType.TANGENT),
                       TokenTest(TokenType.NUMBER, 12)]
        self.check_tokens(tokens, tokens_test)


    def test_basic_6(self):
        tokens = Parser("3x^3 + log10").parse()
        tokens_test = [TokenTest(TokenType.NUMBER, 3),
                       TokenTest(TokenType.MULTIPLICATION),
                       TokenTest(TokenType.X),
                       TokenTest(TokenType.POWER),
                       TokenTest(TokenType.NUMBER, 3),
                       TokenTest(TokenType.PLUS),
                       TokenTest(TokenType.LOG, 10),
                       TokenTest(TokenType.NUMBER, 10)]
        self.check_tokens(tokens, tokens_test)


    def test_basic_7(self):
        tokens = Parser("5/(2x + 6x^2)").parse()
        tokens_test = [TokenTest(TokenType.NUMBER, 5),
                       TokenTest(TokenType.DIVISION),
                       TokenTest(TokenType.BRACKET_LEFT),
                       TokenTest(TokenType.NUMBER, 2),
                       TokenTest(TokenType.MULTIPLICATION),
                       TokenTest(TokenType.X),
                       TokenTest(TokenType.PLUS),
                       TokenTest(TokenType.NUMBER, 6),
                       TokenTest(TokenType.MULTIPLICATION),
                       TokenTest(TokenType.X),
                       TokenTest(TokenType.POWER),
                       TokenTest(TokenType.NUMBER, 2),
                       TokenTest(TokenType.BRACKET_RIGHT)]
        self.check_tokens(tokens, tokens_test)


    def test_basic_8(self):
        tokens = Parser("52/(log350x + 55^2 + cos(20x+6))").parse()
        tokens_test = [TokenTest(TokenType.NUMBER, 52),
                       TokenTest(TokenType.DIVISION),
                       TokenTest(TokenType.BRACKET_LEFT),
                       TokenTest(TokenType.LOG, 10),
                       TokenTest(TokenType.NUMBER, 350),
                       TokenTest(TokenType.MULTIPLICATION),
                       TokenTest(TokenType.X),
                       TokenTest(TokenType.PLUS),
                       TokenTest(TokenType.NUMBER, 55),
                       TokenTest(TokenType.POWER),
                       TokenTest(TokenType.NUMBER, 2),
                       TokenTest(TokenType.PLUS),
                       TokenTest(TokenType.COSINE),
                       TokenTest(TokenType.BRACKET_LEFT),
                       TokenTest(TokenType.NUMBER, 20),
                       TokenTest(TokenType.MULTIPLICATION, 0),
                       TokenTest(TokenType.X),
                       TokenTest(TokenType.PLUS),
                       TokenTest(TokenType.NUMBER, 6),
                       TokenTest(TokenType.BRACKET_RIGHT),
                       TokenTest(TokenType.BRACKET_RIGHT)]
        self.check_tokens(tokens, tokens_test)


    def test_basic_9(self):
        tokens = Parser("x3 + 4x(2x + 1)").parse()
        assert len(tokens) == 15
        self.check_token(tokens[0],  0, TokenType.X)
        self.check_token(tokens[1],  0, TokenType.MULTIPLICATION)
        self.check_token(tokens[2],  3, TokenType.NUMBER)
        self.check_token(tokens[3],  0, TokenType.PLUS)
        self.check_token(tokens[4],  4, TokenType.NUMBER)
        self.check_token(tokens[5],  0, TokenType.MULTIPLICATION)
        self.check_token(tokens[6],  0, TokenType.X)
        self.check_token(tokens[7],  0, TokenType.MULTIPLICATION)
        self.check_token(tokens[8],  0, TokenType.BRACKET_LEFT)
        self.check_token(tokens[9],  2, TokenType.NUMBER)
        self.check_token(tokens[10], 0, TokenType.MULTIPLICATION)
        self.check_token(tokens[11], 0, TokenType.X)
        self.check_token(tokens[12], 0, TokenType.PLUS)
        self.check_token(tokens[13], 1, TokenType.NUMBER)
        self.check_token(tokens[14], 0, TokenType.BRACKET_RIGHT)


    def test_basic_10(self):
        tokens = Parser("(2x + x)(12 - x5)4x").parse()
        assert len(tokens) == 19
        self.check_token(tokens[0],  0, TokenType.BRACKET_LEFT)
        self.check_token(tokens[1],  2, TokenType.NUMBER)
        self.check_token(tokens[2],  0, TokenType.MULTIPLICATION)
        self.check_token(tokens[3],  0, TokenType.X)
        self.check_token(tokens[4],  0, TokenType.PLUS)
        self.check_token(tokens[5],  0, TokenType.X)
        self.check_token(tokens[6],  0, TokenType.BRACKET_RIGHT)
        self.check_token(tokens[7],  0, TokenType.MULTIPLICATION)
        self.check_token(tokens[8],  0, TokenType.BRACKET_LEFT)
        self.check_token(tokens[9],  12, TokenType.NUMBER)
        self.check_token(tokens[10], 0, TokenType.MINUS)
        self.check_token(tokens[11], 0, TokenType.X)
        self.check_token(tokens[12], 0, TokenType.MULTIPLICATION)
        self.check_token(tokens[13], 5, TokenType.NUMBER)
        self.check_token(tokens[14], 0, TokenType.BRACKET_RIGHT)
        self.check_token(tokens[15], 0, TokenType.MULTIPLICATION)
        self.check_token(tokens[16], 4, TokenType.NUMBER)
        self.check_token(tokens[17], 0, TokenType.MULTIPLICATION)
        self.check_token(tokens[18], 0, TokenType.X)


    def test_basic_11(self):
        tokens = Parser("sqrtx + sqrt12").parse()
        assert len(tokens) == 5
        self.check_token(tokens[0], 2, TokenType.ROOT)
        self.check_token(tokens[1], 0, TokenType.X)
        self.check_token(tokens[2], 0, TokenType.PLUS)
        self.check_token(tokens[3], 2, TokenType.ROOT)
        self.check_token(tokens[4], 12, TokenType.NUMBER)


    def test_basic_12(self):
        tokens = Parser("sqrt(x + 4) + sqrt(sinx)").parse()
        assert len(tokens) == 12
        self.check_token(tokens[0],  2, TokenType.ROOT)
        self.check_token(tokens[1],  0, TokenType.BRACKET_LEFT)
        self.check_token(tokens[2],  0, TokenType.X)
        self.check_token(tokens[3],  0, TokenType.PLUS)
        self.check_token(tokens[4],  4, TokenType.NUMBER)
        self.check_token(tokens[5],  0, TokenType.BRACKET_RIGHT)
        self.check_token(tokens[6],  0, TokenType.PLUS)
        self.check_token(tokens[7],  2, TokenType.ROOT)
        self.check_token(tokens[8],  0, TokenType.BRACKET_LEFT)
        self.check_token(tokens[9],  0, TokenType.SINE)
        self.check_token(tokens[10], 0, TokenType.X)
        self.check_token(tokens[11], 0, TokenType.BRACKET_RIGHT)


    def test_negative_1(self):
        tokens = Parser("(-x - 3)4").parse()
        assert len(tokens) == 7
        self.check_token(tokens[0], 0, TokenType.BRACKET_LEFT)
        self.check_token(tokens[1], 0, TokenType.X_NEGATIVE)
        self.check_token(tokens[2], 0, TokenType.MINUS)
        self.check_token(tokens[3], 3, TokenType.NUMBER)
        self.check_token(tokens[4], 0, TokenType.BRACKET_RIGHT)
        self.check_token(tokens[5], 0, TokenType.MULTIPLICATION)
        self.check_token(tokens[6], 4, TokenType.NUMBER)


    def test_negative_2(self):
        tokens = Parser("(x+3)(-5)").parse()
        assert len(tokens) == 9
        self.check_token(tokens[0],  0, TokenType.BRACKET_LEFT)
        self.check_token(tokens[1],  0, TokenType.X)
        self.check_token(tokens[2],  0, TokenType.PLUS)
        self.check_token(tokens[3],  3, TokenType.NUMBER)
        self.check_token(tokens[4],  0, TokenType.BRACKET_RIGHT)
        self.check_token(tokens[5],  0, TokenType.MULTIPLICATION)
        self.check_token(tokens[6],  0, TokenType.BRACKET_LEFT)
        self.check_token(tokens[7], -5, TokenType.NUMBER)
        self.check_token(tokens[8],  0, TokenType.BRACKET_RIGHT)


    def test_negative_3(self):
        tokens = Parser("-x -2(  -7)").parse()
        assert len(tokens) == 7
        self.check_token(tokens[0],  0, TokenType.X_NEGATIVE)
        self.check_token(tokens[1],  0, TokenType.MINUS)
        self.check_token(tokens[2],  2, TokenType.NUMBER)
        self.check_token(tokens[3],  0, TokenType.MULTIPLICATION)
        self.check_token(tokens[4],  0, TokenType.BRACKET_LEFT)
        self.check_token(tokens[5], -7, TokenType.NUMBER)
        self.check_token(tokens[6],  0, TokenType.BRACKET_RIGHT)


    def test_negative_4(self):
        tokens = Parser("-(x^2)").parse()
        assert len(tokens) == 7
        self.check_token(tokens[0], -1, TokenType.NUMBER)
        self.check_token(tokens[1],  0, TokenType.MULTIPLICATION)
        self.check_token(tokens[2],  0, TokenType.BRACKET_LEFT)
        self.check_token(tokens[3],  0, TokenType.X)
        self.check_token(tokens[4],  0, TokenType.POWER)
        self.check_token(tokens[5],  2, TokenType.NUMBER)
        self.check_token(tokens[6],  0, TokenType.BRACKET_RIGHT)


    def test_square_brackets_1(self):
        tokens = Parser("sqrt<2>16").parse()
        assert len(tokens) == 2
        self.check_token(tokens[0], 2, TokenType.ROOT)
        self.check_token(tokens[1], 16, TokenType.NUMBER)


