
from unittest import TestCase
from Parser import Parser
from Token import TokenType
from Token import TokenSymbol


class TestParser(TestCase):

    @staticmethod
    def check_token(token, token_type, token_number, token_symbol):
        assert token.token_type is token_type
        assert token.token_number == token_number
        assert token.token_symbol is token_symbol

    def test_proper_expression_1(self):
        tokens = Parser("2x + 3").parse()
        assert len(tokens) is 4
        self.check_token(tokens[0], TokenType.NUMBER, 2, TokenSymbol.NONE)
        self.check_token(tokens[1], TokenType.SYMBOL, 0, TokenSymbol.X)
        self.check_token(tokens[2], TokenType.SYMBOL, 0, TokenSymbol.PLUS)
        self.check_token(tokens[3], TokenType.NUMBER, 3, TokenSymbol.NONE)

    def test_proper_expression_2(self):
        tokens = Parser("3(4x + cos30)").parse()
        assert len(tokens) is 8
        self.check_token(tokens[0], TokenType.NUMBER,       3,  TokenSymbol.NONE)
        self.check_token(tokens[1], TokenType.BRACKET,      0,  TokenSymbol.BRACKET_LEFT)
        self.check_token(tokens[2], TokenType.NUMBER,       4,  TokenSymbol.NONE)
        self.check_token(tokens[3], TokenType.SYMBOL,       0,  TokenSymbol.X)
        self.check_token(tokens[4], TokenType.SYMBOL,       0,  TokenSymbol.PLUS)
        self.check_token(tokens[5], TokenType.TRIGONOMETRY, 0,  TokenSymbol.COSINE)
        self.check_token(tokens[6], TokenType.NUMBER,       30, TokenSymbol.NONE)
        self.check_token(tokens[7], TokenType.BRACKET,      0,  TokenSymbol.BRACKET_RIGHT)

    def test_proper_expression_3(self):
        tokens = Parser("3x^3 + log10").parse()
        assert len(tokens) is 7
        self.check_token(tokens[0], TokenType.NUMBER, 3,  TokenSymbol.NONE)
        self.check_token(tokens[1], TokenType.SYMBOL, 0,  TokenSymbol.X)
        self.check_token(tokens[2], TokenType.SYMBOL, 0,  TokenSymbol.POWER)
        self.check_token(tokens[3], TokenType.NUMBER, 3,  TokenSymbol.NONE)
        self.check_token(tokens[4], TokenType.SYMBOL, 0,  TokenSymbol.PLUS)
        self.check_token(tokens[5], TokenType.SYMBOL, 0,  TokenSymbol.LOG)
        self.check_token(tokens[6], TokenType.NUMBER, 10, TokenSymbol.NONE)

    def test_proper_expression_4(self):
        tokens = Parser("5/(2x + 6x^2)").parse()
        assert len(tokens) is 11
        self.check_token(tokens[0],  TokenType.NUMBER,  5, TokenSymbol.NONE)
        self.check_token(tokens[1],  TokenType.SYMBOL,  0, TokenSymbol.DIVIDE)
        self.check_token(tokens[2],  TokenType.BRACKET, 0, TokenSymbol.BRACKET_LEFT)
        self.check_token(tokens[3],  TokenType.NUMBER,  2, TokenSymbol.NONE)
        self.check_token(tokens[4],  TokenType.SYMBOL,  0, TokenSymbol.X)
        self.check_token(tokens[5],  TokenType.SYMBOL,  0, TokenSymbol.PLUS)
        self.check_token(tokens[6],  TokenType.NUMBER,  6, TokenSymbol.NONE)
        self.check_token(tokens[7],  TokenType.SYMBOL,  0, TokenSymbol.X)
        self.check_token(tokens[8],  TokenType.SYMBOL,  0, TokenSymbol.POWER)
        self.check_token(tokens[9],  TokenType.NUMBER,  2, TokenSymbol.NONE)
        self.check_token(tokens[10], TokenType.BRACKET, 0, TokenSymbol.BRACKET_RIGHT)

    def test_proper_expression_5(self):
        tokens = Parser("52/(log350x + 55^2 + cos(20x+6))").parse()
        assert len(tokens) is 19
        self.check_token(tokens[0],  TokenType.NUMBER,       52,  TokenSymbol.NONE)
        self.check_token(tokens[1],  TokenType.SYMBOL,       0,   TokenSymbol.DIVIDE)
        self.check_token(tokens[2],  TokenType.BRACKET,      0,   TokenSymbol.BRACKET_LEFT)
        self.check_token(tokens[3],  TokenType.SYMBOL,       0,   TokenSymbol.LOG)
        self.check_token(tokens[4],  TokenType.NUMBER,       350, TokenSymbol.NONE)
        self.check_token(tokens[5],  TokenType.SYMBOL,       0,   TokenSymbol.X)
        self.check_token(tokens[6],  TokenType.SYMBOL,       0,   TokenSymbol.PLUS)
        self.check_token(tokens[7],  TokenType.NUMBER,       55,  TokenSymbol.NONE)
        self.check_token(tokens[8],  TokenType.SYMBOL,       0,   TokenSymbol.POWER)
        self.check_token(tokens[9],  TokenType.NUMBER,       2,   TokenSymbol.NONE)
        self.check_token(tokens[10], TokenType.SYMBOL,       0,   TokenSymbol.PLUS)
        self.check_token(tokens[11], TokenType.TRIGONOMETRY, 0,   TokenSymbol.COSINE)
        self.check_token(tokens[12], TokenType.BRACKET,      0,   TokenSymbol.BRACKET_LEFT)
        self.check_token(tokens[13], TokenType.NUMBER,       20,  TokenSymbol.NONE)
        self.check_token(tokens[14], TokenType.SYMBOL,       0,   TokenSymbol.X)
        self.check_token(tokens[15], TokenType.SYMBOL,       0,   TokenSymbol.PLUS)
        self.check_token(tokens[16], TokenType.NUMBER,       6,   TokenSymbol.NONE)
        self.check_token(tokens[17], TokenType.BRACKET,      0,   TokenSymbol.BRACKET_RIGHT)
        self.check_token(tokens[18], TokenType.BRACKET,      0,   TokenSymbol.BRACKET_RIGHT)

    def test_improper_expression_1(self):
        with self.assertRaises(Exception) as exc:
            Parser("(2x + 3) / ((3x + 4)").parse()
        error = exc.exception
        self.assertEqual(str(error), "Parse expression failed: improper brackets")

    def test_improper_expression_2(self):
        with self.assertRaises(Exception) as exc:
            Parser("12y + 4").parse()
        error = exc.exception
        print(str(error))
        self.assertEqual(str(error), "Parse expression failed: improper symbol at index 2")

    def test_improper_expression_3(self):
        with self.assertRaises(Exception) as exc:
            Parser("tg45 * cor30 - 3").parse()
        error = exc.exception
        self.assertEqual(str(error), "Parse expression failed: improper symbol at index 8 or 9")

    def test_improper_expression_4(self):
        with self.assertRaises(Exception) as exc:
            Parser(")4x(2x +1)").parse()
        error = exc.exception
        self.assertEqual(str(error), "Parse expression failed: improper bracket at index 0")

