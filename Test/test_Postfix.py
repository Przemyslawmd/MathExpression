
from unittest import TestCase
from Tokens.Parser import Parser
from Tokens.TokenGroup import TokenGroup
from Tokens.Token import TokenValue
from Notations.Postfix import Postfix


class TestPostfix(TestCase):


    def test_postfix_1(self):
        tokens = Parser("3 + x * 10 + x").parse()
        tokens_postfix = Postfix().create_postfix(tokens)
        assert tokens_postfix[0].token_number == 3
        assert tokens_postfix[1].token_value is TokenValue.X
        assert tokens_postfix[2].token_number == 10
        assert tokens_postfix[3].token_value is TokenValue.MULTIPLICATION
        assert tokens_postfix[4].token_value is TokenValue.PLUS
        assert tokens_postfix[5].token_value is TokenValue.X
        assert tokens_postfix[6].token_value is TokenValue.PLUS


    def test_postfix_2(self):
        tokens = Parser("cosx * log10 + 12 * x^3").parse()
        tokens_postfix = Postfix().create_postfix(tokens)

        assert tokens_postfix[0].token_value is TokenValue.COSINE
        assert tokens_postfix[1].token_value is TokenValue.X

        assert tokens_postfix[2].token_value is TokenValue.LOG
        assert tokens_postfix[3].token_number == 10

        assert tokens_postfix[4].token_value is TokenValue.MULTIPLICATION

        assert tokens_postfix[5].token_number == 12

        assert tokens_postfix[6].token_value is TokenValue.X
        assert tokens_postfix[7].token_value is TokenValue.POWER
        assert tokens_postfix[8].token_number == 3

        assert tokens_postfix[9].token_value is TokenValue.MULTIPLICATION

        assert tokens_postfix[10].token_value is TokenValue.PLUS

    def test_postfix_3(self):
        tokens = Parser("(3 + x) * (10 + x)").parse()
        tokens_postfix = Postfix().create_postfix(tokens)
        assert len(tokens_postfix) is 7
        assert tokens_postfix[0].token_number == 3
        assert tokens_postfix[1].token_value is TokenValue.X
        assert tokens_postfix[2].token_value is TokenValue.PLUS
        assert tokens_postfix[3].token_number == 10
        assert tokens_postfix[4].token_value is TokenValue.X
        assert tokens_postfix[5].token_value is TokenValue.PLUS
        assert tokens_postfix[6].token_value is TokenValue.MULTIPLICATION


    def test_postfix_4(self):
        tokens = Parser("cos2x * (10x + log12) / cosx").parse()
        tokens_postfix = Postfix().create_postfix(tokens)

        assert tokens_postfix[0].token_value is TokenValue.COSINE
        assert tokens_postfix[1].token_number == 2
        assert tokens_postfix[2].token_value is TokenValue.X

        assert tokens_postfix[3].token_number is 10
        assert tokens_postfix[4].token_value is TokenValue.X

        assert tokens_postfix[5].token_value is TokenValue.LOG
        assert tokens_postfix[6].token_number == 12

        assert tokens_postfix[7].token_value is TokenValue.PLUS

        assert tokens_postfix[8].token_value is TokenValue.MULTIPLICATION

        assert tokens_postfix[9].token_value is TokenValue.COSINE
        assert tokens_postfix[10].token_value is TokenValue.X

        assert tokens_postfix[11].token_value is TokenValue.DIVISION


    def test_postfix_5(self):
        tokens = Parser("tgx * (ctgx + 12x / ctgx)").parse()
        tokens_postfix = Postfix().create_postfix(tokens)

        assert tokens_postfix[0].token_value is TokenValue.TANGENT
        assert tokens_postfix[1].token_value is TokenValue.X

        assert tokens_postfix[2].token_value is TokenValue.COTANGENT
        assert tokens_postfix[3].token_value is TokenValue.X

        assert tokens_postfix[4].token_number == 12
        assert tokens_postfix[5].token_value is TokenValue.X

        assert tokens_postfix[6].token_value is TokenValue.COTANGENT
        assert tokens_postfix[7].token_value is TokenValue.X

        assert tokens_postfix[8].token_value is TokenValue.DIVISION

        assert tokens_postfix[9].token_value is TokenValue.PLUS

        assert tokens_postfix[10].token_value is TokenValue.MULTIPLICATION

    def test_postfix_calculate(self):
        print("test_postfix_calculate")
        tokens = Parser("3 + x * 10 + x").parse()
        postfix = Postfix()
        tokens_postfix = postfix.create_postfix(tokens)
        result = postfix.calculate(2)
        assert result[0] == 25

    def test_postfix_calculate_2(self):
        print("test_postfix_calculate")
        tokens = Parser("(3 + x) * (10 + x)").parse()
        postfix = Postfix()
        tokens_postfix = postfix.create_postfix(tokens)
        result = postfix.calculate(5)
        assert result[0] == 120





