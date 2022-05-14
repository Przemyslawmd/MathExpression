
from unittest import TestCase
from Notations.Postfix import Postfix
from Tokens.Parser import Parser
from Tokens.Token import TokenType


class TestPostfixCreate(TestCase):

    def test_postfix_1(self):
        tokens = Parser("3 + x * 10 + x").parse()
        tokens_postfix = Postfix().create_postfix(tokens)
        assert len(tokens_postfix) == 7
        assert tokens_postfix[0].data == 3
        assert tokens_postfix[1].type is TokenType.X
        assert tokens_postfix[2].data == 10
        assert tokens_postfix[3].type is TokenType.MULTIPLICATION
        assert tokens_postfix[4].type is TokenType.PLUS
        assert tokens_postfix[5].type is TokenType.X
        assert tokens_postfix[6].type is TokenType.PLUS


    def test_postfix_2(self):
        tokens = Parser("sinx + x").parse()
        tokens_postfix = Postfix().create_postfix(tokens)
        assert len(tokens_postfix) == 4
        assert tokens_postfix[0].type is TokenType.X
        assert tokens_postfix[1].type is TokenType.SINE
        assert tokens_postfix[2].type is TokenType.X
        assert tokens_postfix[3].type is TokenType.PLUS


    def test_postfix_3(self):
        tokens = Parser("xcos10").parse()
        tokens_postfix = Postfix().create_postfix(tokens)
        assert len(tokens_postfix) == 4
        assert tokens_postfix[0].type == TokenType.X
        assert tokens_postfix[1].data == 10
        assert tokens_postfix[2].type == TokenType.COSINE
        assert tokens_postfix[3].type is TokenType.MULTIPLICATION


    def test_postfix_4(self):
        tokens = Parser("x^2").parse()
        tokens_postfix = Postfix().create_postfix(tokens)
        assert len(tokens_postfix) == 3
        assert tokens_postfix[0].type == TokenType.X
        assert tokens_postfix[1].type is TokenType.NUMBER and tokens_postfix[1].data == 2
        assert tokens_postfix[2].type == TokenType.POWER


    def test_postfix_5(self):
        tokens = Parser("2x^3").parse()
        tokens_postfix = Postfix().create_postfix(tokens)
        assert len(tokens_postfix) == 5
        assert tokens_postfix[0].type is TokenType.NUMBER and tokens_postfix[0].data == 2
        assert tokens_postfix[1].type == TokenType.X
        assert tokens_postfix[2].type is TokenType.NUMBER and tokens_postfix[2].data == 3
        assert tokens_postfix[3].type == TokenType.POWER
        assert tokens_postfix[4].type is TokenType.MULTIPLICATION


    def test_postfix_6(self):
        tokens = Parser("10tgx - xctgx").parse()
        tokens_postfix = Postfix().create_postfix(tokens)
        assert len(tokens_postfix) == 9
        assert tokens_postfix[0].data == 10
        assert tokens_postfix[1].type is TokenType.X
        assert tokens_postfix[2].type is TokenType.TANGENT
        assert tokens_postfix[3].type is TokenType.MULTIPLICATION
        assert tokens_postfix[4].type is TokenType.X
        assert tokens_postfix[5].type is TokenType.X
        assert tokens_postfix[6].type is TokenType.COTANGENT
        assert tokens_postfix[7].type is TokenType.MULTIPLICATION
        assert tokens_postfix[8].type is TokenType.MINUS


    def test_postfix_7(self):
        tokens = Parser("cosx * log10 + 12x").parse()
        tokens_postfix = Postfix().create_postfix(tokens)
        assert len(tokens_postfix) == 9
        assert tokens_postfix[0].type is TokenType.X
        assert tokens_postfix[1].type is TokenType.COSINE
        assert tokens_postfix[2].type is TokenType.NUMBER and tokens_postfix[2].data == 10
        assert tokens_postfix[3].type is TokenType.LOG
        assert tokens_postfix[4].type is TokenType.MULTIPLICATION
        assert tokens_postfix[5].type is TokenType.NUMBER and tokens_postfix[5].data == 12
        assert tokens_postfix[6].type is TokenType.X
        assert tokens_postfix[7].type is TokenType.MULTIPLICATION
        assert tokens_postfix[8].type is TokenType.PLUS


    def test_postfix_8(self):
        tokens = Parser("(3 + x) * (10 + x)").parse()
        tokens_postfix = Postfix().create_postfix(tokens)
        assert len(tokens_postfix) == 7
        assert tokens_postfix[0].data == 3
        assert tokens_postfix[1].type is TokenType.X
        assert tokens_postfix[2].type is TokenType.PLUS
        assert tokens_postfix[3].data == 10
        assert tokens_postfix[4].type is TokenType.X
        assert tokens_postfix[5].type is TokenType.PLUS
        assert tokens_postfix[6].type is TokenType.MULTIPLICATION


    def test_postfix_9(self):
        tokens = Parser("cosx  (10x + logx) / cosx").parse()
        tokens_postfix = Postfix().create_postfix(tokens)
        assert len(tokens_postfix) == 12
        assert tokens_postfix[0].type is TokenType.X
        assert tokens_postfix[1].type is TokenType.COSINE
        assert tokens_postfix[2].type is TokenType.NUMBER and tokens_postfix[2].data == 10
        assert tokens_postfix[3].type is TokenType.X
        assert tokens_postfix[4].type is TokenType.MULTIPLICATION
        assert tokens_postfix[5].type is TokenType.X
        assert tokens_postfix[6].type is TokenType.LOG
        assert tokens_postfix[7].type is TokenType.PLUS
        assert tokens_postfix[8].type is TokenType.MULTIPLICATION
        assert tokens_postfix[9].type is TokenType.X
        assert tokens_postfix[10].type is TokenType.COSINE
        assert tokens_postfix[11].type is TokenType.DIVISION


    def test_postfix_10(self):
        tokens = Parser("tgx * (ctgx + 12x / ctgx)").parse()
        tokens_postfix = Postfix().create_postfix(tokens)
        assert len(tokens_postfix) == 12
        assert tokens_postfix[0].type is TokenType.X
        assert tokens_postfix[1].type is TokenType.TANGENT
        assert tokens_postfix[2].type is TokenType.X
        assert tokens_postfix[3].type is TokenType.COTANGENT
        assert tokens_postfix[4].data == 12
        assert tokens_postfix[5].type is TokenType.X
        assert tokens_postfix[6].type is TokenType.MULTIPLICATION
        assert tokens_postfix[7].type is TokenType.X
        assert tokens_postfix[8].type is TokenType.COTANGENT
        assert tokens_postfix[9].type is TokenType.DIVISION
        assert tokens_postfix[10].type is TokenType.PLUS
        assert tokens_postfix[11].type is TokenType.MULTIPLICATION


