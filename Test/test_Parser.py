
from unittest import TestCase
from Tokens.Parser import Parser
from Tokens.Token import TokenValue


class TestParser(TestCase):

    @staticmethod
    def check_token(token, token_number, token_value):
        assert token.number == token_number
        assert token.value is token_value


    def test_expression_1(self):
        tokens = Parser("2x + 3").parse()
        assert len(tokens) == 5
        self.check_token(tokens[0], 2, TokenValue.NUMBER)
        self.check_token(tokens[1], 0, TokenValue.MULTIPLICATION)
        self.check_token(tokens[2], 0, TokenValue.X)
        self.check_token(tokens[3], 0, TokenValue.PLUS)
        self.check_token(tokens[4], 3, TokenValue.NUMBER)


    def test_expression_2(self):
        tokens = Parser("3(4x + cos30)").parse()
        assert len(tokens) == 10
        self.check_token(tokens[0], 3,  TokenValue.NUMBER)
        self.check_token(tokens[1], 0,  TokenValue.MULTIPLICATION)
        self.check_token(tokens[2], 0,  TokenValue.BRACKET_LEFT)
        self.check_token(tokens[3], 4,  TokenValue.NUMBER)
        self.check_token(tokens[4], 0,  TokenValue.MULTIPLICATION)
        self.check_token(tokens[5], 0,  TokenValue.X)
        self.check_token(tokens[6], 0,  TokenValue.PLUS)
        self.check_token(tokens[7], 0,  TokenValue.COSINE)
        self.check_token(tokens[8], 30, TokenValue.NUMBER)
        self.check_token(tokens[9], 0,  TokenValue.BRACKET_RIGHT)


    def test_expression_3(self):
        tokens = Parser("3(4x + 12cos30)").parse()
        assert len(tokens) == 12
        self.check_token(tokens[0],  3,  TokenValue.NUMBER)
        self.check_token(tokens[1],  0,  TokenValue.MULTIPLICATION)
        self.check_token(tokens[2],  0,  TokenValue.BRACKET_LEFT)
        self.check_token(tokens[3],  4,  TokenValue.NUMBER)
        self.check_token(tokens[4],  0,  TokenValue.MULTIPLICATION)
        self.check_token(tokens[5],  0,  TokenValue.X)
        self.check_token(tokens[6],  0,  TokenValue.PLUS)
        self.check_token(tokens[7],  12, TokenValue.NUMBER)
        self.check_token(tokens[8],  0,  TokenValue.MULTIPLICATION)
        self.check_token(tokens[9],  0,  TokenValue.COSINE)
        self.check_token(tokens[10], 30, TokenValue.NUMBER)
        self.check_token(tokens[11], 0,  TokenValue.BRACKET_RIGHT)


    def test_expression_4(self):
        tokens = Parser("(4 + x)sinx").parse()
        assert len(tokens) == 8
        self.check_token(tokens[0],  0, TokenValue.BRACKET_LEFT)
        self.check_token(tokens[1],  4, TokenValue.NUMBER)
        self.check_token(tokens[2],  0, TokenValue.PLUS)
        self.check_token(tokens[3],  0, TokenValue.X)
        self.check_token(tokens[4],  0, TokenValue.BRACKET_RIGHT)
        self.check_token(tokens[5],  0, TokenValue.MULTIPLICATION)
        self.check_token(tokens[6],  0, TokenValue.SINE)
        self.check_token(tokens[7],  0, TokenValue.X)


    def test_expression_5(self):
        tokens = Parser("xtg12").parse()
        assert len(tokens) == 4
        self.check_token(tokens[0],  0, TokenValue.X)
        self.check_token(tokens[1],  0, TokenValue.MULTIPLICATION)
        self.check_token(tokens[2],  0, TokenValue.TANGENT)
        self.check_token(tokens[3], 12, TokenValue.NUMBER)


    def test_expression_6(self):
        tokens = Parser("3x^3 + log10").parse()
        assert len(tokens) == 8
        self.check_token(tokens[0], 3,  TokenValue.NUMBER)
        self.check_token(tokens[1], 0,  TokenValue.MULTIPLICATION)
        self.check_token(tokens[2], 0,  TokenValue.X)
        self.check_token(tokens[3], 0,  TokenValue.POWER)
        self.check_token(tokens[4], 3,  TokenValue.NUMBER)
        self.check_token(tokens[5], 0,  TokenValue.PLUS)
        self.check_token(tokens[6], 0,  TokenValue.LOG)
        self.check_token(tokens[7], 10, TokenValue.NUMBER)


    def test_expression_7(self):
        tokens = Parser("5/(2x + 6x^2)").parse()
        assert len(tokens) == 13
        self.check_token(tokens[0],  5, TokenValue.NUMBER)
        self.check_token(tokens[1],  0, TokenValue.DIVISION)
        self.check_token(tokens[2],  0, TokenValue.BRACKET_LEFT)
        self.check_token(tokens[3],  2, TokenValue.NUMBER)
        self.check_token(tokens[4],  0, TokenValue.MULTIPLICATION)
        self.check_token(tokens[5],  0, TokenValue.X)
        self.check_token(tokens[6],  0, TokenValue.PLUS)
        self.check_token(tokens[7],  6, TokenValue.NUMBER)
        self.check_token(tokens[8],  0, TokenValue.MULTIPLICATION)
        self.check_token(tokens[9],  0, TokenValue.X)
        self.check_token(tokens[10], 0, TokenValue.POWER)
        self.check_token(tokens[11], 2, TokenValue.NUMBER)
        self.check_token(tokens[12], 0, TokenValue.BRACKET_RIGHT)


    def test_expression_8(self):
        tokens = Parser("52/(log350x + 55^2 + cos(20x+6))").parse()
        assert len(tokens) == 21
        self.check_token(tokens[0],  52,  TokenValue.NUMBER)
        self.check_token(tokens[1],  0,   TokenValue.DIVISION)
        self.check_token(tokens[2],  0,   TokenValue.BRACKET_LEFT)
        self.check_token(tokens[3],  0,   TokenValue.LOG)
        self.check_token(tokens[4],  350, TokenValue.NUMBER)
        self.check_token(tokens[5],  0,   TokenValue.MULTIPLICATION)
        self.check_token(tokens[6],  0,   TokenValue.X)
        self.check_token(tokens[7],  0,   TokenValue.PLUS)
        self.check_token(tokens[8],  55,  TokenValue.NUMBER)
        self.check_token(tokens[9],  0,   TokenValue.POWER)
        self.check_token(tokens[10], 2,   TokenValue.NUMBER)
        self.check_token(tokens[11], 0,   TokenValue.PLUS)
        self.check_token(tokens[12], 0,   TokenValue.COSINE)
        self.check_token(tokens[13], 0,   TokenValue.BRACKET_LEFT)
        self.check_token(tokens[14], 20,  TokenValue.NUMBER)
        self.check_token(tokens[15], 0,   TokenValue.MULTIPLICATION)
        self.check_token(tokens[16], 0,   TokenValue.X)
        self.check_token(tokens[17], 0,   TokenValue.PLUS)
        self.check_token(tokens[18], 6,   TokenValue.NUMBER)
        self.check_token(tokens[19], 0,   TokenValue.BRACKET_RIGHT)
        self.check_token(tokens[20], 0,   TokenValue.BRACKET_RIGHT)


    def test_expression_9(self):
        tokens = Parser("x3 + 4x(2x + 1)").parse()
        assert len(tokens) == 15
        self.check_token(tokens[0],  0, TokenValue.X)
        self.check_token(tokens[1],  0, TokenValue.MULTIPLICATION)
        self.check_token(tokens[2],  3, TokenValue.NUMBER)
        self.check_token(tokens[3],  0, TokenValue.PLUS)
        self.check_token(tokens[4],  4, TokenValue.NUMBER)
        self.check_token(tokens[5],  0, TokenValue.MULTIPLICATION)
        self.check_token(tokens[6],  0, TokenValue.X)
        self.check_token(tokens[7],  0, TokenValue.MULTIPLICATION)
        self.check_token(tokens[8],  0, TokenValue.BRACKET_LEFT)
        self.check_token(tokens[9],  2, TokenValue.NUMBER)
        self.check_token(tokens[10], 0, TokenValue.MULTIPLICATION)
        self.check_token(tokens[11], 0, TokenValue.X)
        self.check_token(tokens[12], 0, TokenValue.PLUS)
        self.check_token(tokens[13], 1, TokenValue.NUMBER)
        self.check_token(tokens[14], 0, TokenValue.BRACKET_RIGHT)


    def test_expression_10(self):
        tokens = Parser("(2x + x)(12 - x5)4x").parse()
        assert len(tokens) == 19
        self.check_token(tokens[0],  0,  TokenValue.BRACKET_LEFT)
        self.check_token(tokens[1],  2,  TokenValue.NUMBER)
        self.check_token(tokens[2],  0,  TokenValue.MULTIPLICATION)
        self.check_token(tokens[3],  0,  TokenValue.X)
        self.check_token(tokens[4],  0,  TokenValue.PLUS)
        self.check_token(tokens[5],  0,  TokenValue.X)
        self.check_token(tokens[6],  0,  TokenValue.BRACKET_RIGHT)
        self.check_token(tokens[7],  0,  TokenValue.MULTIPLICATION)
        self.check_token(tokens[8],  0,  TokenValue.BRACKET_LEFT)
        self.check_token(tokens[9],  12, TokenValue.NUMBER)
        self.check_token(tokens[10], 0,  TokenValue.MINUS)
        self.check_token(tokens[11], 0,  TokenValue.X)
        self.check_token(tokens[12], 0,  TokenValue.MULTIPLICATION)
        self.check_token(tokens[13], 5,  TokenValue.NUMBER)
        self.check_token(tokens[14], 0,  TokenValue.BRACKET_RIGHT)
        self.check_token(tokens[15], 0,  TokenValue.MULTIPLICATION)
        self.check_token(tokens[16], 4,  TokenValue.NUMBER)
        self.check_token(tokens[17], 0,  TokenValue.MULTIPLICATION)
        self.check_token(tokens[18], 0,  TokenValue.X)


    def test_expression_with_negative_1(self):
        tokens = Parser("(-x - 3)4").parse()
        assert len(tokens) == 7
        self.check_token(tokens[0], 0, TokenValue.BRACKET_LEFT)
        self.check_token(tokens[1], 0, TokenValue.X_NEGATIVE)
        self.check_token(tokens[2], 0, TokenValue.MINUS)
        self.check_token(tokens[3], 3, TokenValue.NUMBER)
        self.check_token(tokens[4], 0, TokenValue.BRACKET_RIGHT)
        self.check_token(tokens[5], 0, TokenValue.MULTIPLICATION)
        self.check_token(tokens[6], 4, TokenValue.NUMBER)


    def test_expression_with_negative_2(self):
        tokens = Parser("(x+3)(-5)").parse()
        assert len(tokens) == 9
        self.check_token(tokens[0],  0, TokenValue.BRACKET_LEFT)
        self.check_token(tokens[1],  0, TokenValue.X)
        self.check_token(tokens[2],  0, TokenValue.PLUS)
        self.check_token(tokens[3],  3, TokenValue.NUMBER)
        self.check_token(tokens[4],  0, TokenValue.BRACKET_RIGHT)
        self.check_token(tokens[5],  0, TokenValue.MULTIPLICATION)
        self.check_token(tokens[6],  0, TokenValue.BRACKET_LEFT)
        self.check_token(tokens[7], -5, TokenValue.NUMBER)
        self.check_token(tokens[8],  0, TokenValue.BRACKET_RIGHT)


    def test_expression_with_negative_3(self):
        tokens = Parser("-x -2(  -7)").parse()
        assert len(tokens) == 7
        self.check_token(tokens[0],  0, TokenValue.X_NEGATIVE)
        self.check_token(tokens[1],  0, TokenValue.MINUS)
        self.check_token(tokens[2],  2, TokenValue.NUMBER)
        self.check_token(tokens[3],  0, TokenValue.MULTIPLICATION)
        self.check_token(tokens[4],  0, TokenValue.BRACKET_LEFT)
        self.check_token(tokens[5], -7, TokenValue.NUMBER)
        self.check_token(tokens[6],  0, TokenValue.BRACKET_RIGHT)


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


    def test_improper_negative_expression_1(self):
        with self.assertRaises(Exception) as exc:
            Parser("(-*5 + x)").parse()
        error = exc.exception
        self.assertEqual(str(error), "Parse failed: improper usage of negative symbol")


    def test_improper_negative_expression_2(self):
        with self.assertRaises(Exception) as exc:
            Parser("5x * x-").parse()
        error = exc.exception
        self.assertEqual(str(error), "Parse failed: improper usage of negative symbol")


    def test_improper_negative_expression_3(self):
        with self.assertRaises(Exception) as exc:
            Parser("(5x + x)(5 + 3-)").parse()
        error = exc.exception
        self.assertEqual(str(error), "Parse failed: improper usage of negative symbol")


