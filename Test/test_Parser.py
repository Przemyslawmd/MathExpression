
from unittest import TestCase
from Parser import Parser
from Token import Token


class TestParser(TestCase):

    def test_proper_expression_1(self):
        tokens = Parser("2x + 3").parse()
        assert len(tokens) is 4
        assert tokens[0] is Token.TWO
        assert tokens[1] is Token.X
        assert tokens[2] is Token.PLUS
        assert tokens[3] is Token.THREE

    def test_proper_expression_2(self):
        tokens = Parser("3(4x + cos30)").parse()
        assert len(tokens) is 9
        assert tokens[0] is Token.THREE
        assert tokens[1] is Token.BRACKET_LEFT
        assert tokens[2] is Token.FOUR
        assert tokens[3] is Token.X
        assert tokens[4] is Token.PLUS
        assert tokens[5] is Token.COSINE
        assert tokens[6] is Token.THREE
        assert tokens[7] is Token.ZERO
        assert tokens[8] is Token.BRACKET_RIGHT

    def test_proper_expression_3(self):
        tokens = Parser("3x^3 + log10").parse()
        assert len(tokens) is 8
        assert tokens[0] is Token.THREE
        assert tokens[1] is Token.X
        assert tokens[2] is Token.POWER
        assert tokens[3] is Token.THREE
        assert tokens[4] is Token.PLUS
        assert tokens[5] is Token.LOG
        assert tokens[6] is Token.ONE
        assert tokens[7] is Token.ZERO

    def test_proper_expression_4(self):
        tokens = Parser("5/(2x + 6x^2)").parse()
        assert len(tokens) is 11
        assert tokens[0] is Token.FIVE
        assert tokens[1] is Token.DIVIDE
        assert tokens[2] is Token.BRACKET_LEFT
        assert tokens[3] is Token.TWO
        assert tokens[4] is Token.X
        assert tokens[5] is Token.PLUS
        assert tokens[6] is Token.SIX
        assert tokens[7] is Token.X
        assert tokens[8] is Token.POWER
        assert tokens[9] is Token.TWO
        assert tokens[10] is Token.BRACKET_RIGHT

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
