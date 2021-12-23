
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


    #def test_postfix_2(self):
    #    tokens = Parser("cosx * log10 + 12 * x^3").parse()
    #    tokens_postfix = Postfix().create_postfix(tokens)
    #    assert len(tokens_postfix) == 11
    #    assert tokens_postfix[0].token_value is TokenValue.COSINE
    #    assert tokens_postfix[1].token_value is TokenValue.X
    #    assert tokens_postfix[2].token_value is TokenValue.LOG
    #    assert tokens_postfix[3].token_number == 10
    #    assert tokens_postfix[4].token_value is TokenValue.MULTIPLICATION
    #    assert tokens_postfix[5].token_number == 12
    #    assert tokens_postfix[6].token_value is TokenValue.X
    #    assert tokens_postfix[7].token_value is TokenValue.POWER
    #    assert tokens_postfix[8].token_number == 3
    #    assert tokens_postfix[9].token_value is TokenValue.MULTIPLICATION
    #    assert tokens_postfix[10].token_value is TokenValue.PLUS


    def test_postfix_5(self):
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


    #def test_postfix_4(self):
    #    tokens = Parser("cos2x * (10x + log12) / cosx").parse()
    #    tokens_postfix = Postfix().create_postfix(tokens)
    #    assert len(tokens_postfix) == 14
    #    assert tokens_postfix[0].token_value is TokenValue.COSINE
    #    assert tokens_postfix[1].token_number == 2
    #    assert tokens_postfix[2].token_value is TokenValue.X
    #    assert tokens_postfix[3].token_value is TokenValue.MULTIPLICATION
    #    assert tokens_postfix[4].token_number == 10
    #    assert tokens_postfix[5].token_value is TokenValue.X
    #    assert tokens_postfix[6].token_value is TokenValue.MULTIPLICATION
    #    assert tokens_postfix[7].token_value is TokenValue.LOG
    #    assert tokens_postfix[8].token_number == 12
    #    assert tokens_postfix[9].token_value is TokenValue.PLUS
    #    assert tokens_postfix[10].token_value is TokenValue.MULTIPLICATION
    #    assert tokens_postfix[11].token_value is TokenValue.COSINE
    #    assert tokens_postfix[12].token_value is TokenValue.X
    #    assert tokens_postfix[13].token_value is TokenValue.DIVISION


    def test_postfix_6(self):
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
        assert result[0][0] == 25
        assert result[1][0] == 36


    def test_postfix_calculate_2(self):
        tokens = Parser("(3 + x) * (10 + x)").parse()
        postfix = Postfix()
        postfix.create_postfix(tokens)
        result = postfix.calculate(5, 6)
        assert result[0][0] == 120
        assert result[1][0] == 144


    def test_postfix_calculate_3(self):
        tokens = Parser("2 * (3 + x) * 4").parse()
        postfix = Postfix()
        postfix.create_postfix(tokens)
        result = postfix.calculate(2, 5)
        assert result[0][0] == 40
        assert result[1][0] == 48
        assert result[2][0] == 56
        assert result[3][0] == 64


    def test_postfix_calculate_4(self):
        tokens = Parser("(4x + x3)2x").parse()
        postfix = Postfix()
        postfix.create_postfix(tokens)
        result = postfix.calculate(0, 5)
        assert result[0][0] == 0
        assert result[1][0] == 14
        assert result[2][0] == 56
        assert result[3][0] == 126
        assert result[4][0] == 224
        assert result[5][0] == 350


    def test_postfix_calculate_5(self):
        tokens = Parser("(2 - x3)4").parse()
        postfix = Postfix()
        postfix.create_postfix(tokens)
        result = postfix.calculate(10, 12)
        assert result[0][0] == -112
        assert result[1][0] == -124
        assert result[2][0] == -136


    def test_postfix_calculate_6(self):
        tokens = Parser("(-x - 3)4").parse()
        postfix = Postfix()
        postfix.create_postfix(tokens)
        result = postfix.calculate(5, 7)
        assert result[0][0] == -32
        assert result[1][0] == -36
        assert result[2][0] == -40


    def test_postfix_calculate_7(self):
        tokens = Parser("(x +3)(-5)").parse()
        postfix = Postfix()
        postfix.create_postfix(tokens)
        result = postfix.calculate(100, 103)
        assert result[0][0] == -515
        assert result[1][0] == -520
        assert result[2][0] == -525
        assert result[3][0] == -530


    def test_postfix_calculate_8(self):
        tokens = Parser("(-x -2)(-7)").parse()
        postfix = Postfix()
        postfix.create_postfix(tokens)
        result = postfix.calculate(-2, 2)
        assert result[0][0] == 0
        assert result[1][0] == 7
        assert result[2][0] == 14
        assert result[3][0] == 21
        assert result[4][0] == 28


    def test_postfix_calculate_9(self):
        tokens = Parser("sinx + x").parse()
        postfix = Postfix()
        postfix.create_postfix(tokens)
        result = postfix.calculate(30, 30)
        assert result[0][0] == 30.5


    def test_postfix_calculate_10(self):
        tokens = Parser("xcos10").parse()
        postfix = Postfix()
        postfix.create_postfix(tokens)
        result = postfix.calculate(10, 14)
        assert result[0][0] == 9.85
        assert result[1][0] == 10.83
        assert result[2][0] == 11.82
        assert result[3][0] == 12.8
        assert result[4][0] == 13.79


    def test_postfix_calculate_11(self):
        tokens = Parser("10tgx - xctgx").parse()
        postfix = Postfix()
        postfix.create_postfix(tokens)
        result = postfix.calculate(100, 104)
        assert result[0][0] == -39.08
        assert result[1][0] == -31.81
        assert result[2][0] == -25.37
        assert result[3][0] == -19.54
        assert result[4][0] == -14.18


