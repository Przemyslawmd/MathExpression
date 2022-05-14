
from unittest import TestCase
from Notations.Postfix import Postfix
from Tokens.Parser import Parser
from Tokens.Token import TokenType


class TestPostfixCalculate(TestCase):

    def test_postfix_calculate_1(self):
        tokens = Parser("3 + x * 10 + x").parse()
        postfix = Postfix()
        postfix.create_postfix(tokens)
        result = postfix.calculate(2, 3)
        assert result[0] == 25
        assert result[1] == 36


    def test_postfix_calculate_2(self):
        tokens = Parser("(3 + x) * (10 + x)").parse()
        postfix = Postfix()
        postfix.create_postfix(tokens)
        result = postfix.calculate(5, 6)
        assert result[0] == 120
        assert result[1] == 144


    def test_postfix_calculate_3(self):
        tokens = Parser("2 * (3 + x) * 4").parse()
        postfix = Postfix()
        postfix.create_postfix(tokens)
        result = postfix.calculate(2, 5)
        assert result[0] == 40
        assert result[1] == 48
        assert result[2] == 56
        assert result[3] == 64


    def test_postfix_calculate_4(self):
        tokens = Parser("(4x + x3)2x").parse()
        postfix = Postfix()
        postfix.create_postfix(tokens)
        result = postfix.calculate(0, 5)
        assert result[0] == 0
        assert result[1] == 14
        assert result[2] == 56
        assert result[3] == 126
        assert result[4] == 224
        assert result[5] == 350


    def test_postfix_calculate_5(self):
        tokens = Parser("(2 - x3)4").parse()
        postfix = Postfix()
        postfix.create_postfix(tokens)
        result = postfix.calculate(10, 12)
        assert result[0] == -112
        assert result[1] == -124
        assert result[2] == -136


    def test_postfix_calculate_6(self):
        tokens = Parser("(-x - 3)4").parse()
        postfix = Postfix()
        postfix.create_postfix(tokens)
        result = postfix.calculate(5, 7)
        assert result[0] == -32
        assert result[1] == -36
        assert result[2] == -40


    def test_postfix_calculate_7(self):
        tokens = Parser("(x +3)(-5)").parse()
        postfix = Postfix()
        postfix.create_postfix(tokens)
        result = postfix.calculate(100, 103)
        assert result[0] == -515
        assert result[1] == -520
        assert result[2] == -525
        assert result[3] == -530


    def test_postfix_calculate_8(self):
        tokens = Parser("(-x -2)(-7)").parse()
        postfix = Postfix()
        postfix.create_postfix(tokens)
        result = postfix.calculate(-2, 2)
        assert result[0] == 0
        assert result[1] == 7
        assert result[2] == 14
        assert result[3] == 21
        assert result[4] == 28


    def test_postfix_calculate_9(self):
        tokens = Parser("sinx + x").parse()
        postfix = Postfix()
        postfix.create_postfix(tokens)
        result = postfix.calculate(30, 30)
        assert result[0] == 30.5


    def test_postfix_calculate_10(self):
        tokens = Parser("xcos10").parse()
        postfix = Postfix()
        postfix.create_postfix(tokens)
        result = postfix.calculate(10, 14)
        assert result[0] == 9.8481
        assert result[1] == 10.8329
        assert result[2] == 11.8177
        assert result[3] == 12.8025
        assert result[4] == 13.7873


    def test_postfix_calculate_11(self):
        tokens = Parser("10tgx - xctgx").parse()
        postfix = Postfix()
        postfix.create_postfix(tokens)
        result = postfix.calculate(100, 104)
        assert result[0] == -39.0801
        assert result[1] == -31.8131
        assert result[2] == -25.3655
        assert result[3] == -19.5353
        assert result[4] == -14.1777


    def test_postfix_calculate_12(self):
        tokens = Parser("sqrtx + 10").parse()
        postfix = Postfix()
        postfix.create_postfix(tokens)
        result = postfix.calculate(16, 20)
        assert result[0] == 14.0
        assert result[1] == 14.1231
        assert result[2] == 14.2426
        assert result[3] == 14.3589
        assert result[4] == 14.4721


    def test_postfix_calculate_13(self):
        tokens = Parser("x + 2sqrt4").parse()
        postfix = Postfix()
        postfix.create_postfix(tokens)
        result = postfix.calculate(10, 15)
        assert result[0] == 14
        assert result[1] == 15
        assert result[2] == 16
        assert result[3] == 17
        assert result[4] == 18

