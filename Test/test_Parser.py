
from unittest import TestCase
from Tokens.Parser import Parser
from Tokens.Token import TokenType, TokenValue


class TestParser(TestCase):

    @staticmethod
    def check_token(token, token_type, token_number, token_value):
        assert token.token_type is token_type
        assert token.token_number == token_number
        assert token.token_value is token_value


    def test_proper_expression_1(self):
        tokens = Parser("2x + 3").parse()
        assert len(tokens) == 5
        self.check_token(tokens[0], TokenType.NUMBER,    2, TokenValue.NONE)
        self.check_token(tokens[1], TokenType.OPERATION, 0, TokenValue.MULTIPLICATION)
        self.check_token(tokens[2], TokenType.OTHER,     0, TokenValue.X)
        self.check_token(tokens[3], TokenType.OPERATION, 0, TokenValue.PLUS)
        self.check_token(tokens[4], TokenType.NUMBER,    3, TokenValue.NONE)


    def test_proper_expression_2(self):
        tokens = Parser("3(4x + cos30)").parse()
        assert len(tokens) == 10
        self.check_token(tokens[0], TokenType.NUMBER,       3,  TokenValue.NONE)
        self.check_token(tokens[1], TokenType.OPERATION,    0,  TokenValue.MULTIPLICATION)
        self.check_token(tokens[2], TokenType.BRACKET,      0,  TokenValue.BRACKET_LEFT)
        self.check_token(tokens[3], TokenType.NUMBER,       4,  TokenValue.NONE)
        self.check_token(tokens[4], TokenType.OPERATION,    0, TokenValue.MULTIPLICATION)
        self.check_token(tokens[5], TokenType.OTHER,        0,  TokenValue.X)
        self.check_token(tokens[6], TokenType.OPERATION,    0,  TokenValue.PLUS)
        self.check_token(tokens[7], TokenType.TRIGONOMETRY, 0,  TokenValue.COSINE)
        self.check_token(tokens[8], TokenType.NUMBER,       30, TokenValue.NONE)
        self.check_token(tokens[9], TokenType.BRACKET,      0,  TokenValue.BRACKET_RIGHT)


    def test_proper_expression_3(self):
        tokens = Parser("3x^3 + log10").parse()
        assert len(tokens) == 8
        self.check_token(tokens[0], TokenType.NUMBER,    3,  TokenValue.NONE)
        self.check_token(tokens[1], TokenType.OPERATION, 0, TokenValue.MULTIPLICATION)
        self.check_token(tokens[2], TokenType.OTHER,     0,  TokenValue.X)
        self.check_token(tokens[3], TokenType.OTHER,     0,  TokenValue.POWER)
        self.check_token(tokens[4], TokenType.NUMBER,    3,  TokenValue.NONE)
        self.check_token(tokens[5], TokenType.OPERATION, 0,  TokenValue.PLUS)
        self.check_token(tokens[6], TokenType.OTHER,     0,  TokenValue.LOG)
        self.check_token(tokens[7], TokenType.NUMBER,    10, TokenValue.NONE)


    def test_proper_expression_4(self):
        tokens = Parser("5/(2x + 6x^2)").parse()
        assert len(tokens) == 13
        self.check_token(tokens[0],  TokenType.NUMBER,    5, TokenValue.NONE)
        self.check_token(tokens[1],  TokenType.OPERATION, 0, TokenValue.DIVISION)
        self.check_token(tokens[2],  TokenType.BRACKET,   0, TokenValue.BRACKET_LEFT)
        self.check_token(tokens[3],  TokenType.NUMBER,    2, TokenValue.NONE)
        self.check_token(tokens[4],  TokenType.OPERATION, 0, TokenValue.MULTIPLICATION)
        self.check_token(tokens[5],  TokenType.OTHER,     0, TokenValue.X)
        self.check_token(tokens[6],  TokenType.OPERATION, 0, TokenValue.PLUS)
        self.check_token(tokens[7],  TokenType.NUMBER,    6, TokenValue.NONE)
        self.check_token(tokens[8],  TokenType.OPERATION, 0, TokenValue.MULTIPLICATION)
        self.check_token(tokens[9],  TokenType.OTHER,     0, TokenValue.X)
        self.check_token(tokens[10], TokenType.OTHER,     0, TokenValue.POWER)
        self.check_token(tokens[11], TokenType.NUMBER,    2, TokenValue.NONE)
        self.check_token(tokens[12], TokenType.BRACKET,   0, TokenValue.BRACKET_RIGHT)


    def test_proper_expression_5(self):
        tokens = Parser("52/(log350x + 55^2 + cos(20x+6))").parse()
        assert len(tokens) == 21
        self.check_token(tokens[0],  TokenType.NUMBER,       52,  TokenValue.NONE)
        self.check_token(tokens[1],  TokenType.OPERATION,    0,   TokenValue.DIVISION)
        self.check_token(tokens[2],  TokenType.BRACKET,      0,   TokenValue.BRACKET_LEFT)
        self.check_token(tokens[3],  TokenType.OTHER,        0,   TokenValue.LOG)
        self.check_token(tokens[4],  TokenType.NUMBER,       350, TokenValue.NONE)
        self.check_token(tokens[5],  TokenType.OPERATION,    0, TokenValue.MULTIPLICATION)
        self.check_token(tokens[6],  TokenType.OTHER,        0,   TokenValue.X)
        self.check_token(tokens[7],  TokenType.OPERATION,    0,   TokenValue.PLUS)
        self.check_token(tokens[8],  TokenType.NUMBER,       55,  TokenValue.NONE)
        self.check_token(tokens[9],  TokenType.OTHER,        0,   TokenValue.POWER)
        self.check_token(tokens[10], TokenType.NUMBER,       2,   TokenValue.NONE)
        self.check_token(tokens[11], TokenType.OPERATION,    0,   TokenValue.PLUS)
        self.check_token(tokens[12], TokenType.TRIGONOMETRY, 0,   TokenValue.COSINE)
        self.check_token(tokens[13], TokenType.BRACKET,      0,   TokenValue.BRACKET_LEFT)
        self.check_token(tokens[14], TokenType.NUMBER,       20,  TokenValue.NONE)
        self.check_token(tokens[15], TokenType.OPERATION,    0, TokenValue.MULTIPLICATION)
        self.check_token(tokens[16], TokenType.OTHER,        0,   TokenValue.X)
        self.check_token(tokens[17], TokenType.OPERATION,    0,   TokenValue.PLUS)
        self.check_token(tokens[18], TokenType.NUMBER,       6,   TokenValue.NONE)
        self.check_token(tokens[19], TokenType.BRACKET,      0,   TokenValue.BRACKET_RIGHT)
        self.check_token(tokens[20], TokenType.BRACKET,      0,   TokenValue.BRACKET_RIGHT)


    def test_proper_expression_6(self):
        tokens = Parser("x3 + 4x(2x + 1)").parse()
        assert len(tokens) == 15
        self.check_token(tokens[0],  TokenType.OTHER,     0, TokenValue.X)
        self.check_token(tokens[1],  TokenType.OPERATION, 0, TokenValue.MULTIPLICATION)
        self.check_token(tokens[2],  TokenType.NUMBER,    3, TokenValue.NONE)
        self.check_token(tokens[3],  TokenType.OPERATION, 0, TokenValue.PLUS)
        self.check_token(tokens[4],  TokenType.NUMBER,    4, TokenValue.NONE)
        self.check_token(tokens[5],  TokenType.OPERATION, 0, TokenValue.MULTIPLICATION)
        self.check_token(tokens[6],  TokenType.OTHER,     0, TokenValue.X)
        self.check_token(tokens[7],  TokenType.OPERATION, 0, TokenValue.MULTIPLICATION)
        self.check_token(tokens[8],  TokenType.BRACKET,   0, TokenValue.BRACKET_LEFT)
        self.check_token(tokens[9],  TokenType.NUMBER,    2, TokenValue.NONE)
        self.check_token(tokens[10], TokenType.OPERATION, 0, TokenValue.MULTIPLICATION)
        self.check_token(tokens[11], TokenType.OTHER,     0, TokenValue.X)
        self.check_token(tokens[12], TokenType.OPERATION, 0, TokenValue.PLUS)
        self.check_token(tokens[13], TokenType.NUMBER,    1, TokenValue.NONE)
        self.check_token(tokens[14], TokenType.BRACKET,   0, TokenValue.BRACKET_RIGHT)


    def test_proper_expression_7(self):
        tokens = Parser("(2x + x)(12 - x5)4x").parse()
        assert len(tokens) == 19
        self.check_token(tokens[0],  TokenType.BRACKET,   0, TokenValue.BRACKET_LEFT)
        self.check_token(tokens[1],  TokenType.NUMBER,    2,  TokenValue.NONE)
        self.check_token(tokens[2],  TokenType.OPERATION, 0,   TokenValue.MULTIPLICATION)
        self.check_token(tokens[3],  TokenType.OTHER,     0, TokenValue.X)
        self.check_token(tokens[4],  TokenType.OPERATION, 0, TokenValue.PLUS)
        self.check_token(tokens[5],  TokenType.OTHER,     0, TokenValue.X)
        self.check_token(tokens[6],  TokenType.BRACKET,   0, TokenValue.BRACKET_RIGHT)
        self.check_token(tokens[7],  TokenType.OPERATION, 0, TokenValue.MULTIPLICATION)
        self.check_token(tokens[8],  TokenType.BRACKET,   0, TokenValue.BRACKET_LEFT)
        self.check_token(tokens[9],  TokenType.NUMBER,    12, TokenValue.NONE)
        self.check_token(tokens[10], TokenType.OPERATION, 0, TokenValue.MINUS)
        self.check_token(tokens[11], TokenType.OTHER,     0, TokenValue.X)
        self.check_token(tokens[12], TokenType.OPERATION, 0, TokenValue.MULTIPLICATION)
        self.check_token(tokens[13], TokenType.NUMBER,    5, TokenValue.NONE)
        self.check_token(tokens[14], TokenType.BRACKET,   0, TokenValue.BRACKET_RIGHT)
        self.check_token(tokens[15], TokenType.OPERATION, 0, TokenValue.MULTIPLICATION)
        self.check_token(tokens[16], TokenType.NUMBER,    4, TokenValue.NONE)
        self.check_token(tokens[17], TokenType.OPERATION, 0, TokenValue.MULTIPLICATION)
        self.check_token(tokens[18], TokenType.OTHER,     0, TokenValue.X)


    def test_improper_expression_1(self):
        with self.assertRaises(Exception) as exc:
            Parser("(2x + 3) / ((3x + 4)").parse()
        error = exc.exception
        self.assertEqual(str(error), "Parse failed: improper brackets")


    def test_improper_expression_2(self):
        with self.assertRaises(Exception) as exc:
            Parser("12y + 4").parse()
        error = exc.exception
        self.assertEqual(str(error), "Parse failed: improper symbol at index 2")


    def test_improper_expression_3(self):
        with self.assertRaises(Exception) as exc:
            Parser("tg45 * cor30 - 3").parse()
        error = exc.exception
        self.assertEqual(str(error), "Parse failed: improper symbol at index 6 or 7")


    def test_improper_expression_4(self):
        with self.assertRaises(Exception) as exc:
            Parser(")4x(2x +1)").parse()
        error = exc.exception
        self.assertEqual(str(error), "Parse failed: improper bracket at index 0")

