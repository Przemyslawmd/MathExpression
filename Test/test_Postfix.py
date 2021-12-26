
from unittest import TestCase
from Notations.Postfix import Postfix
from Tokens.Parser import Parser
from Tokens.Token import TokenValue


class TestPostfix(TestCase):

    def test_postfix_1(self):
        tokens = Parser("3 + x * 10 + x").parse()
        tokens_postfix = Postfix().create_postfix(tokens)
        assert len(tokens_postfix) == 7
        assert tokens_postfix[0].number == 3
        assert tokens_postfix[1].value is TokenValue.X
        assert tokens_postfix[2].number == 10
        assert tokens_postfix[3].value is TokenValue.MULTIPLICATION
        assert tokens_postfix[4].value is TokenValue.PLUS
        assert tokens_postfix[5].value is TokenValue.X
        assert tokens_postfix[6].value is TokenValue.PLUS


    def test_postfix_2(self):
        tokens = Parser("sinx + x").parse()
        tokens_postfix = Postfix().create_postfix(tokens)
        assert len(tokens_postfix) == 4
        assert tokens_postfix[0].value is TokenValue.X
        assert tokens_postfix[1].value is TokenValue.SINE
        assert tokens_postfix[2].value is TokenValue.X
        assert tokens_postfix[3].value is TokenValue.PLUS


    def test_postfix_3(self):
        tokens = Parser("xcos10").parse()
        tokens_postfix = Postfix().create_postfix(tokens)
        assert len(tokens_postfix) == 4
        assert tokens_postfix[0].value == TokenValue.X
        assert tokens_postfix[1].number == 10
        assert tokens_postfix[2].value == TokenValue.COSINE
        assert tokens_postfix[3].value is TokenValue.MULTIPLICATION


    def test_postfix_4(self):
        tokens = Parser("x^2").parse()
        tokens_postfix = Postfix().create_postfix(tokens)
        assert len(tokens_postfix) == 3
        assert tokens_postfix[0].value == TokenValue.X
        assert tokens_postfix[1].value is TokenValue.NUMBER and tokens_postfix[1].number == 2
        assert tokens_postfix[2].value == TokenValue.POWER


    def test_postfix_5(self):
        tokens = Parser("2x^3").parse()
        tokens_postfix = Postfix().create_postfix(tokens)
        assert len(tokens_postfix) == 5
        assert tokens_postfix[0].value is TokenValue.NUMBER and tokens_postfix[0].number == 2
        assert tokens_postfix[1].value == TokenValue.X
        assert tokens_postfix[2].value is TokenValue.NUMBER and tokens_postfix[2].number == 3
        assert tokens_postfix[3].value == TokenValue.POWER
        assert tokens_postfix[4].value is TokenValue.MULTIPLICATION


    def test_postfix_6(self):
        tokens = Parser("10tgx - xctgx").parse()
        tokens_postfix = Postfix().create_postfix(tokens)
        assert len(tokens_postfix) == 9
        assert tokens_postfix[0].number == 10
        assert tokens_postfix[1].value is TokenValue.X
        assert tokens_postfix[2].value is TokenValue.TANGENT
        assert tokens_postfix[3].value is TokenValue.MULTIPLICATION
        assert tokens_postfix[4].value is TokenValue.X
        assert tokens_postfix[5].value is TokenValue.X
        assert tokens_postfix[6].value is TokenValue.COTANGENT
        assert tokens_postfix[7].value is TokenValue.MULTIPLICATION
        assert tokens_postfix[8].value is TokenValue.MINUS


    def test_postfix_7(self):
        tokens = Parser("cosx * log10 + 12x").parse()
        tokens_postfix = Postfix().create_postfix(tokens)
        assert len(tokens_postfix) == 9
        assert tokens_postfix[0].value is TokenValue.X
        assert tokens_postfix[1].value is TokenValue.COSINE
        assert tokens_postfix[2].value is TokenValue.NUMBER and tokens_postfix[2].number == 10
        assert tokens_postfix[3].value is TokenValue.LOG
        assert tokens_postfix[4].value is TokenValue.MULTIPLICATION
        assert tokens_postfix[5].value is TokenValue.NUMBER and tokens_postfix[5].number == 12
        assert tokens_postfix[6].value is TokenValue.X
        assert tokens_postfix[7].value is TokenValue.MULTIPLICATION
        assert tokens_postfix[8].value is TokenValue.PLUS


    def test_postfix_8(self):
        tokens = Parser("(3 + x) * (10 + x)").parse()
        tokens_postfix = Postfix().create_postfix(tokens)
        assert len(tokens_postfix) == 7
        assert tokens_postfix[0].number == 3
        assert tokens_postfix[1].value is TokenValue.X
        assert tokens_postfix[2].value is TokenValue.PLUS
        assert tokens_postfix[3].number == 10
        assert tokens_postfix[4].value is TokenValue.X
        assert tokens_postfix[5].value is TokenValue.PLUS
        assert tokens_postfix[6].value is TokenValue.MULTIPLICATION


    def test_postfix_9(self):
        tokens = Parser("cosx  (10x + logx) / cosx").parse()
        tokens_postfix = Postfix().create_postfix(tokens)
        assert len(tokens_postfix) == 12
        assert tokens_postfix[0].value is TokenValue.X
        assert tokens_postfix[1].value is TokenValue.COSINE
        assert tokens_postfix[2].value is TokenValue.NUMBER and tokens_postfix[2].number == 10
        assert tokens_postfix[3].value is TokenValue.X
        assert tokens_postfix[4].value is TokenValue.MULTIPLICATION
        assert tokens_postfix[5].value is TokenValue.X
        assert tokens_postfix[6].value is TokenValue.LOG
        assert tokens_postfix[7].value is TokenValue.PLUS
        assert tokens_postfix[8].value is TokenValue.MULTIPLICATION
        assert tokens_postfix[9].value is TokenValue.X
        assert tokens_postfix[10].value is TokenValue.COSINE
        assert tokens_postfix[11].value is TokenValue.DIVISION


    def test_postfix_10(self):
        tokens = Parser("tgx * (ctgx + 12x / ctgx)").parse()
        tokens_postfix = Postfix().create_postfix(tokens)
        assert len(tokens_postfix) == 12
        assert tokens_postfix[0].value is TokenValue.X
        assert tokens_postfix[1].value is TokenValue.TANGENT
        assert tokens_postfix[2].value is TokenValue.X
        assert tokens_postfix[3].value is TokenValue.COTANGENT
        assert tokens_postfix[4].number == 12
        assert tokens_postfix[5].value is TokenValue.X
        assert tokens_postfix[6].value is TokenValue.MULTIPLICATION
        assert tokens_postfix[7].value is TokenValue.X
        assert tokens_postfix[8].value is TokenValue.COTANGENT
        assert tokens_postfix[9].value is TokenValue.DIVISION
        assert tokens_postfix[10].value is TokenValue.PLUS
        assert tokens_postfix[11].value is TokenValue.MULTIPLICATION


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
        assert result[0] == 9.85
        assert result[1] == 10.83
        assert result[2] == 11.82
        assert result[3] == 12.8
        assert result[4] == 13.79


    def test_postfix_calculate_11(self):
        tokens = Parser("10tgx - xctgx").parse()
        postfix = Postfix()
        postfix.create_postfix(tokens)
        result = postfix.calculate(100, 104)
        assert result[0] == -39.08
        assert result[1] == -31.81
        assert result[2] == -25.37
        assert result[3] == -19.54
        assert result[4] == -14.18


