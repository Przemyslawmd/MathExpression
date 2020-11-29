
from unittest import TestCase
from Tokens.Parser import Parser
from Tokens.TokenGroup import TokenGroup
from Tokens.Token import TokenValue
from Notations.Postfix import Postfix


class TestPostfix(TestCase):

    def test_postfix_1(self):
        tokens = Parser("3 + x * 10 + x").parse()
        tokens_grouped = TokenGroup().create_tokens(tokens)
        tokens_postfix = Postfix().create_postfix(tokens_grouped)
        assert len(tokens_postfix) is 7
        assert tokens_postfix[0][0].token_number == 3
        assert tokens_postfix[1][0].token_value is TokenValue.X
        assert tokens_postfix[2][0].token_number == 10
        assert tokens_postfix[3].token_value is TokenValue.MULTIPLICATION
        assert tokens_postfix[4].token_value is TokenValue.PLUS
        assert tokens_postfix[5][0].token_value is TokenValue.X
        assert tokens_postfix[6].token_value is TokenValue.PLUS


    def test_postfix_2(self):
        tokens = Parser("cosx * log10 + 12 * x^3").parse()
        tokens_grouped = TokenGroup().create_tokens(tokens)
        tokens_postfix = Postfix().create_postfix(tokens_grouped)
        assert len(tokens_postfix) is 7

        assert len(tokens_postfix[0]) == 2
        assert tokens_postfix[0][0].token_value is TokenValue.COSINE
        assert tokens_postfix[0][1].token_value is TokenValue.X

        assert len(tokens_postfix[1]) == 2
        assert tokens_postfix[1][0].token_value is TokenValue.LOG
        assert tokens_postfix[1][1].token_number == 10

        assert tokens_postfix[2].token_value is TokenValue.MULTIPLICATION

        assert len(tokens_postfix[3]) == 1
        assert tokens_postfix[3][0].token_number == 12

        assert len(tokens_postfix[4]) == 3
        assert tokens_postfix[4][0].token_value is TokenValue.X
        assert tokens_postfix[4][1].token_value is TokenValue.POWER
        assert tokens_postfix[4][2].token_number == 3

        assert tokens_postfix[5].token_value is TokenValue.MULTIPLICATION

        assert tokens_postfix[6].token_value is TokenValue.PLUS


    def test_postfix_3(self):
        tokens = Parser("(3 + x) * (10 + x)").parse()
        tokens_grouped = TokenGroup().create_tokens(tokens)
        tokens_postfix = Postfix().create_postfix(tokens_grouped)
        assert len(tokens_postfix) is 7
        assert tokens_postfix[0][0].token_number == 3
        assert tokens_postfix[1][0].token_value is TokenValue.X
        assert tokens_postfix[2].token_value is TokenValue.PLUS
        assert tokens_postfix[3][0].token_number == 10
        assert tokens_postfix[4][0].token_value is TokenValue.X
        assert tokens_postfix[5].token_value is TokenValue.PLUS
        assert tokens_postfix[6].token_value is TokenValue.MULTIPLICATION


    def test_postfix_4(self):
        tokens = Parser("cos2x * (10x + log12) / cosx").parse()
        tokens_grouped = TokenGroup().create_tokens(tokens)
        tokens_postfix = Postfix().create_postfix(tokens_grouped)
        assert len(tokens_postfix) is 7

        assert len(tokens_postfix[0]) == 3
        assert tokens_postfix[0][0].token_value is TokenValue.COSINE
        assert tokens_postfix[0][1].token_number == 2
        assert tokens_postfix[0][2].token_value is TokenValue.X

        assert len(tokens_postfix[1]) == 2
        assert tokens_postfix[1][0].token_number is 10
        assert tokens_postfix[1][1].token_value is TokenValue.X

        assert len(tokens_postfix[2]) == 2
        assert tokens_postfix[2][0].token_value is TokenValue.LOG
        assert tokens_postfix[2][1].token_number == 12

        assert tokens_postfix[3].token_value is TokenValue.PLUS

        assert tokens_postfix[4].token_value is TokenValue.MULTIPLICATION

        assert len(tokens_postfix[5]) == 2
        assert tokens_postfix[5][0].token_value is TokenValue.COSINE
        assert tokens_postfix[5][1].token_value is TokenValue.X

        assert tokens_postfix[6].token_value is TokenValue.DIVISION


    def test_postfix_5(self):
        tokens = Parser("tgx * (ctgx + 12x / ctgx)").parse()
        tokens_grouped = TokenGroup().create_tokens(tokens)
        tokens_postfix = Postfix().create_postfix(tokens_grouped)
        assert len(tokens_postfix) is 7

        assert len(tokens_postfix[0]) == 2
        assert tokens_postfix[0][0].token_value is TokenValue.TANGENT
        assert tokens_postfix[0][1].token_value is TokenValue.X

        assert len(tokens_postfix[1]) == 2
        assert tokens_postfix[1][0].token_value is TokenValue.COTANGENT
        assert tokens_postfix[1][1].token_value is TokenValue.X

        assert len(tokens_postfix[2]) == 2
        assert tokens_postfix[2][0].token_number == 12
        assert tokens_postfix[2][1].token_value is TokenValue.X

        assert len(tokens_postfix[3]) == 2
        assert tokens_postfix[3][0].token_value is TokenValue.COTANGENT
        assert tokens_postfix[3][1].token_value is TokenValue.X

        assert tokens_postfix[4].token_value is TokenValue.DIVISION

        assert tokens_postfix[5].token_value is TokenValue.PLUS

        assert tokens_postfix[6].token_value is TokenValue.MULTIPLICATION


