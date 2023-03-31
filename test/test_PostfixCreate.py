
from collections import namedtuple

from unittest import TestCase

from postfix.postfix import Postfix
from tokens.parser import Parser
from tokens.token import TokenType
from testUtils import TokenTest, check_tokens



class TestPostfixCreate(TestCase):


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
        check_tokens(tokens_postfix, tokens_test)


    def test_postfix_2(self):
        tokens = Parser("sinx + x").parse()
        tokens_postfix = Postfix().create_postfix(tokens)
        tokens_test = [TokenTest(TokenType.X),
                       TokenTest(TokenType.SINE),
                       TokenTest(TokenType.X),
                       TokenTest(TokenType.PLUS)]
        check_tokens(tokens_postfix, tokens_test)


    def test_postfix_3(self):
        tokens = Parser("xcos10").parse()
        tokens_postfix = Postfix().create_postfix(tokens)
        tokens_test = [TokenTest(TokenType.X),
                       TokenTest(TokenType.NUMBER, 10),
                       TokenTest(TokenType.COSINE),
                       TokenTest(TokenType.MULTIPLICATION)]
        check_tokens(tokens_postfix, tokens_test)


    def test_postfix_4(self):
        tokens = Parser("x^2").parse()
        tokens_postfix = Postfix().create_postfix(tokens)
        tokens_test = [TokenTest(TokenType.X),
                       TokenTest(TokenType.NUMBER, 2),
                       TokenTest(TokenType.POWER)]
        check_tokens(tokens_postfix, tokens_test)


    def test_postfix_5(self):
        tokens = Parser("2x^3").parse()
        tokens_postfix = Postfix().create_postfix(tokens)
        tokens_test = [TokenTest(TokenType.NUMBER, 2),
                       TokenTest(TokenType.X),
                       TokenTest(TokenType.NUMBER, 3),
                       TokenTest(TokenType.POWER),
                       TokenTest(TokenType.MULTIPLICATION)]
        check_tokens(tokens_postfix, tokens_test)


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
        check_tokens(tokens_postfix, tokens_test)


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
        check_tokens(tokens_postfix, tokens_test)


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
        check_tokens(tokens_postfix, tokens_test)


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
        check_tokens(tokens_postfix, tokens_test)


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
        check_tokens(tokens_postfix, tokens_test)


