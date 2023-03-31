
from collections import namedtuple

from unittest import TestCase

from postfix.postfix import Postfix
from tokens.parser import Parser
from tokens.token import TokenType


TokenTest = namedtuple('TokenTest', 'type data', defaults=[0])


class TestPostfixCreate(TestCase):


    @staticmethod
    def check_tokens(tokens, tokens_test):
        assert len(tokens) == len(tokens_test)
        for token, token_test in zip(tokens, tokens_test):
            assert token.type == token_test.type
            assert token.data == token_test.data


    def test_postfix_1(self):
        tokens = Parser("3 + x * 10 + x").parse()
        tokens_postfix = Postfix().create_postfix(tokens)
        tokens_test = [TokenTest(TokenType.NUMBER, 3),
                       TokenTest(TokenType.X),
                       TokenTest(TokenType.NUMBER, 10),
                       TokenTest(TokenType.MULTIPLICATION),
                       TokenTest(TokenType.PLUS),
                       TokenTest(TokenType.X),
                       TokenTest(TokenType.PLUS)]
        self.check_tokens(tokens_postfix, tokens_test)


    def test_postfix_2(self):
        tokens = Parser("sinx + x").parse()
        tokens_postfix = Postfix().create_postfix(tokens)
        tokens_test = [TokenTest(TokenType.X),
                       TokenTest(TokenType.SINE),
                       TokenTest(TokenType.X),
                       TokenTest(TokenType.PLUS)]
        self.check_tokens(tokens_postfix, tokens_test)


    def test_postfix_3(self):
        tokens = Parser("xcos10").parse()
        tokens_postfix = Postfix().create_postfix(tokens)
        tokens_test = [TokenTest(TokenType.X),
                       TokenTest(TokenType.NUMBER, 10),
                       TokenTest(TokenType.COSINE),
                       TokenTest(TokenType.MULTIPLICATION)]
        self.check_tokens(tokens_postfix, tokens_test)


    def test_postfix_4(self):
        tokens = Parser("x^2").parse()
        tokens_postfix = Postfix().create_postfix(tokens)
        tokens_test = [TokenTest(TokenType.X),
                       TokenTest(TokenType.NUMBER, 2),
                       TokenTest(TokenType.POWER)]
        self.check_tokens(tokens_postfix, tokens_test)


    def test_postfix_5(self):
        tokens = Parser("2x^3").parse()
        tokens_postfix = Postfix().create_postfix(tokens)
        tokens_test = [TokenTest(TokenType.NUMBER, 2),
                       TokenTest(TokenType.X),
                       TokenTest(TokenType.NUMBER, 3),
                       TokenTest(TokenType.POWER),
                       TokenTest(TokenType.MULTIPLICATION)]
        self.check_tokens(tokens_postfix, tokens_test)


    def test_postfix_6(self):
        tokens = Parser("10tgx - xctgx").parse()
        tokens_postfix = Postfix().create_postfix(tokens)
        tokens_test = [TokenTest(TokenType.NUMBER, 10),
                       TokenTest(TokenType.X),
                       TokenTest(TokenType.TANGENT),
                       TokenTest(TokenType.MULTIPLICATION),
                       TokenTest(TokenType.X),
                       TokenTest(TokenType.X),
                       TokenTest(TokenType.COTANGENT),
                       TokenTest(TokenType.MULTIPLICATION),
                       TokenTest(TokenType.MINUS)]
        self.check_tokens(tokens_postfix, tokens_test)


    def test_postfix_7(self):
        tokens = Parser("cosx * log10 + 12x").parse()
        tokens_postfix = Postfix().create_postfix(tokens)
        tokens_test = [TokenTest(TokenType.X),
                       TokenTest(TokenType.COSINE),
                       TokenTest(TokenType.NUMBER, 10),
                       TokenTest(TokenType.LOG, 10),
                       TokenTest(TokenType.MULTIPLICATION),
                       TokenTest(TokenType.NUMBER, 12),
                       TokenTest(TokenType.X),
                       TokenTest(TokenType.MULTIPLICATION),
                       TokenTest(TokenType.PLUS)]
        self.check_tokens(tokens_postfix, tokens_test)


    def test_postfix_8(self):
        tokens = Parser("(3 + x) * (10 + x)").parse()
        tokens_postfix = Postfix().create_postfix(tokens)
        tokens_test = [TokenTest(TokenType.NUMBER, 3),
                       TokenTest(TokenType.X),
                       TokenTest(TokenType.PLUS),
                       TokenTest(TokenType.NUMBER, 10),
                       TokenTest(TokenType.X),
                       TokenTest(TokenType.PLUS),
                       TokenTest(TokenType.MULTIPLICATION)]
        self.check_tokens(tokens_postfix, tokens_test)


    def test_postfix_9(self):
        tokens = Parser("cosx  (10x + logx) / cosx").parse()
        tokens_postfix = Postfix().create_postfix(tokens)
        tokens_test = [TokenTest(TokenType.X),
                       TokenTest(TokenType.COSINE),
                       TokenTest(TokenType.NUMBER, 10),
                       TokenTest(TokenType.X),
                       TokenTest(TokenType.MULTIPLICATION),
                       TokenTest(TokenType.X),
                       TokenTest(TokenType.LOG, 10),
                       TokenTest(TokenType.PLUS),
                       TokenTest(TokenType.MULTIPLICATION),
                       TokenTest(TokenType.X),
                       TokenTest(TokenType.COSINE),
                       TokenTest(TokenType.DIVISION)]
        self.check_tokens(tokens_postfix, tokens_test)


    def test_postfix_10(self):
        tokens = Parser("tgx * (ctgx + 12x / ctgx)").parse()
        tokens_postfix = Postfix().create_postfix(tokens)
        tokens_test = [TokenTest(TokenType.X),
                       TokenTest(TokenType.TANGENT),
                       TokenTest(TokenType.X),
                       TokenTest(TokenType.COTANGENT),
                       TokenTest(TokenType.NUMBER, 12),
                       TokenTest(TokenType.X),
                       TokenTest(TokenType.MULTIPLICATION),
                       TokenTest(TokenType.X),
                       TokenTest(TokenType.COTANGENT),
                       TokenTest(TokenType.DIVISION),
                       TokenTest(TokenType.PLUS),
                       TokenTest(TokenType.MULTIPLICATION)]
        self.check_tokens(tokens_postfix, tokens_test)


