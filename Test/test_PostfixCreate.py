
from unittest import TestCase
from Notations.Postfix import Postfix
from Tokens.Parser import Parser
from Tokens.Token import TokenValue


class TestPostfixCreate(TestCase):

    def test_postfix_1(self):
        tokens = Parser("3 + x * 10 + x").parse()
        tokens_postfix = Postfix().create_postfix(tokens)
        assert len(tokens_postfix) == 7
        assert tokens_postfix[0].data == 3
        assert tokens_postfix[1].value is TokenValue.X
        assert tokens_postfix[2].data == 10
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
        assert tokens_postfix[1].data == 10
        assert tokens_postfix[2].value == TokenValue.COSINE
        assert tokens_postfix[3].value is TokenValue.MULTIPLICATION


    def test_postfix_4(self):
        tokens = Parser("x^2").parse()
        tokens_postfix = Postfix().create_postfix(tokens)
        assert len(tokens_postfix) == 3
        assert tokens_postfix[0].value == TokenValue.X
        assert tokens_postfix[1].value is TokenValue.NUMBER and tokens_postfix[1].data == 2
        assert tokens_postfix[2].value == TokenValue.POWER


    def test_postfix_5(self):
        tokens = Parser("2x^3").parse()
        tokens_postfix = Postfix().create_postfix(tokens)
        assert len(tokens_postfix) == 5
        assert tokens_postfix[0].value is TokenValue.NUMBER and tokens_postfix[0].data == 2
        assert tokens_postfix[1].value == TokenValue.X
        assert tokens_postfix[2].value is TokenValue.NUMBER and tokens_postfix[2].data == 3
        assert tokens_postfix[3].value == TokenValue.POWER
        assert tokens_postfix[4].value is TokenValue.MULTIPLICATION


    def test_postfix_6(self):
        tokens = Parser("10tgx - xctgx").parse()
        tokens_postfix = Postfix().create_postfix(tokens)
        assert len(tokens_postfix) == 9
        assert tokens_postfix[0].data == 10
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
        assert tokens_postfix[2].value is TokenValue.NUMBER and tokens_postfix[2].data == 10
        assert tokens_postfix[3].value is TokenValue.LOG
        assert tokens_postfix[4].value is TokenValue.MULTIPLICATION
        assert tokens_postfix[5].value is TokenValue.NUMBER and tokens_postfix[5].data == 12
        assert tokens_postfix[6].value is TokenValue.X
        assert tokens_postfix[7].value is TokenValue.MULTIPLICATION
        assert tokens_postfix[8].value is TokenValue.PLUS


    def test_postfix_8(self):
        tokens = Parser("(3 + x) * (10 + x)").parse()
        tokens_postfix = Postfix().create_postfix(tokens)
        assert len(tokens_postfix) == 7
        assert tokens_postfix[0].data == 3
        assert tokens_postfix[1].value is TokenValue.X
        assert tokens_postfix[2].value is TokenValue.PLUS
        assert tokens_postfix[3].data == 10
        assert tokens_postfix[4].value is TokenValue.X
        assert tokens_postfix[5].value is TokenValue.PLUS
        assert tokens_postfix[6].value is TokenValue.MULTIPLICATION


    def test_postfix_9(self):
        tokens = Parser("cosx  (10x + logx) / cosx").parse()
        tokens_postfix = Postfix().create_postfix(tokens)
        assert len(tokens_postfix) == 12
        assert tokens_postfix[0].value is TokenValue.X
        assert tokens_postfix[1].value is TokenValue.COSINE
        assert tokens_postfix[2].value is TokenValue.NUMBER and tokens_postfix[2].data == 10
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
        assert tokens_postfix[4].data == 12
        assert tokens_postfix[5].value is TokenValue.X
        assert tokens_postfix[6].value is TokenValue.MULTIPLICATION
        assert tokens_postfix[7].value is TokenValue.X
        assert tokens_postfix[8].value is TokenValue.COTANGENT
        assert tokens_postfix[9].value is TokenValue.DIVISION
        assert tokens_postfix[10].value is TokenValue.PLUS
        assert tokens_postfix[11].value is TokenValue.MULTIPLICATION


