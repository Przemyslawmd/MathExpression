
from unittest import TestCase

from tokens.parser import Parser
from tokens.token import TokenType
from testUtils import TokenTest, check_tokens


class TestParser(TestCase):


    def test_basic_1(self):
        tokens = Parser("2x + 3").parse()
        tokens_test = [TokenTest(TokenType.NUMBER, 2),
                       TokenTest(TokenType.MULTIPLICATION),
                       TokenTest(TokenType.X),
                       TokenTest(TokenType.PLUS),
                       TokenTest(TokenType.NUMBER, 3)]
        check_tokens(tokens, tokens_test)


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
        check_tokens(tokens, tokens_test)


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
        check_tokens(tokens, tokens_test)


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
        check_tokens(tokens, tokens_test)


    def test_basic_5(self):
        tokens = Parser("xtg12").parse()
        tokens_test = [TokenTest(TokenType.X),
                       TokenTest(TokenType.MULTIPLICATION),
                       TokenTest(TokenType.TANGENT),
                       TokenTest(TokenType.NUMBER, 12)]
        check_tokens(tokens, tokens_test)


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
        check_tokens(tokens, tokens_test)


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
        check_tokens(tokens, tokens_test)


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
        check_tokens(tokens, tokens_test)


    def test_basic_9(self):
        tokens = Parser("x3 + 4x(2x + 1)").parse()
        tokens_test = [TokenTest(TokenType.X),
                       TokenTest(TokenType.MULTIPLICATION),
                       TokenTest(TokenType.NUMBER, 3),
                       TokenTest(TokenType.PLUS),
                       TokenTest(TokenType.NUMBER, 4),
                       TokenTest(TokenType.MULTIPLICATION),
                       TokenTest(TokenType.X),
                       TokenTest(TokenType.MULTIPLICATION),
                       TokenTest(TokenType.BRACKET_LEFT),
                       TokenTest(TokenType.NUMBER, 2),
                       TokenTest(TokenType.MULTIPLICATION),
                       TokenTest(TokenType.X),
                       TokenTest(TokenType.PLUS),
                       TokenTest(TokenType.NUMBER, 1),
                       TokenTest(TokenType.BRACKET_RIGHT)]
        check_tokens(tokens, tokens_test)


    def test_basic_10(self):
        tokens = Parser("(2x + x)(12 - x5)4x").parse()
        tokens_test = [TokenTest(TokenType.BRACKET_LEFT),
                       TokenTest(TokenType.NUMBER, 2),
                       TokenTest(TokenType.MULTIPLICATION),
                       TokenTest(TokenType.X),
                       TokenTest(TokenType.PLUS),
                       TokenTest(TokenType.X),
                       TokenTest(TokenType.BRACKET_RIGHT),
                       TokenTest(TokenType.MULTIPLICATION),
                       TokenTest(TokenType.BRACKET_LEFT),
                       TokenTest(TokenType.NUMBER, 12),
                       TokenTest(TokenType.MINUS),
                       TokenTest(TokenType.X),
                       TokenTest(TokenType.MULTIPLICATION, 0),
                       TokenTest(TokenType.NUMBER, 5),
                       TokenTest(TokenType.BRACKET_RIGHT),
                       TokenTest(TokenType.MULTIPLICATION),
                       TokenTest(TokenType.NUMBER, 4),
                       TokenTest(TokenType.MULTIPLICATION),
                       TokenTest(TokenType.X)]
        check_tokens(tokens, tokens_test)


    def test_basic_11(self):
        tokens = Parser("sqrtx + sqrt12").parse()
        tokens_test = [TokenTest(TokenType.ROOT, 2),
                       TokenTest(TokenType.X),
                       TokenTest(TokenType.PLUS),
                       TokenTest(TokenType.ROOT, 2),
                       TokenTest(TokenType.NUMBER, 12)]
        check_tokens(tokens, tokens_test)


    def test_basic_12(self):
        tokens = Parser("sqrt(x + 4) + sqrt(sinx)").parse()
        tokens_test = [TokenTest(TokenType.ROOT, 2),
                       TokenTest(TokenType.BRACKET_LEFT),
                       TokenTest(TokenType.X),
                       TokenTest(TokenType.PLUS),
                       TokenTest(TokenType.NUMBER, 4),
                       TokenTest(TokenType.BRACKET_RIGHT),
                       TokenTest(TokenType.PLUS),
                       TokenTest(TokenType.ROOT, 2),
                       TokenTest(TokenType.BRACKET_LEFT),
                       TokenTest(TokenType.SINE),
                       TokenTest(TokenType.X),
                       TokenTest(TokenType.BRACKET_RIGHT)]
        check_tokens(tokens, tokens_test)


    def test_negative_1(self):
        tokens = Parser("(-x - 3)4").parse()
        tokens_test = [TokenTest(TokenType.BRACKET_LEFT),
                       TokenTest(TokenType.X_NEGATIVE),
                       TokenTest(TokenType.MINUS),
                       TokenTest(TokenType.NUMBER, 3),
                       TokenTest(TokenType.BRACKET_RIGHT),
                       TokenTest(TokenType.MULTIPLICATION),
                       TokenTest(TokenType.NUMBER, 4)]
        check_tokens(tokens, tokens_test)


    def test_negative_2(self):
        tokens = Parser("(x+3)(-5)").parse()
        tokens_test = [TokenTest(TokenType.BRACKET_LEFT),
                       TokenTest(TokenType.X),
                       TokenTest(TokenType.PLUS),
                       TokenTest(TokenType.NUMBER, 3),
                       TokenTest(TokenType.BRACKET_RIGHT),
                       TokenTest(TokenType.MULTIPLICATION),
                       TokenTest(TokenType.BRACKET_LEFT),
                       TokenTest(TokenType.NUMBER, -5),
                       TokenTest(TokenType.BRACKET_RIGHT)]
        check_tokens(tokens, tokens_test)


    def test_negative_3(self):
        tokens = Parser("-x -2(  -7)").parse()
        tokens_test = [TokenTest(TokenType.X_NEGATIVE),
                       TokenTest(TokenType.MINUS),
                       TokenTest(TokenType.NUMBER, 2),
                       TokenTest(TokenType.MULTIPLICATION),
                       TokenTest(TokenType.BRACKET_LEFT),
                       TokenTest(TokenType.NUMBER, -7),
                       TokenTest(TokenType.BRACKET_RIGHT)]
        check_tokens(tokens, tokens_test)


    def test_negative_4(self):
        tokens = Parser("-(x^2)").parse()
        tokens_test = [TokenTest(TokenType.NUMBER, -1),
                       TokenTest(TokenType.MULTIPLICATION),
                       TokenTest(TokenType.BRACKET_LEFT),
                       TokenTest(TokenType.X),
                       TokenTest(TokenType.POWER),
                       TokenTest(TokenType.NUMBER, 2),
                       TokenTest(TokenType.BRACKET_RIGHT)]
        check_tokens(tokens, tokens_test)


    def test_angle_brackets_1(self):
        tokens = Parser("sqrt<2>16").parse()
        tokens_test = [TokenTest(TokenType.ROOT, 2),
                       TokenTest(TokenType.NUMBER, 16)]
        check_tokens(tokens, tokens_test)


