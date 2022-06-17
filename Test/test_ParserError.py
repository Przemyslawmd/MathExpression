from unittest import TestCase
from Token.Parser import Parser
from Errors import ErrorType, ErrorMessage


class TestParserError(TestCase):

    def test_basic_1(self):
        with self.assertRaises(Exception) as exc:
            Parser("(2x + 3) / ((3x + 4)").parse()
        error = exc.exception
        self.assertEqual(str(error), ErrorMessage[ErrorType.PARSER_BRACKET])


    def test_basic_2(self):
        with self.assertRaises(Exception) as exc:
            Parser("12y + 4").parse()
        error = exc.exception
        self.assertEqual(str(error), ErrorMessage[ErrorType.PARSER_SYMBOL] + ": y")


    def test_basic_3(self):
        with self.assertRaises(Exception) as exc:
            Parser("tg45 * cor30 - 3").parse()
        error = exc.exception
        self.assertEqual(str(error), ErrorMessage[ErrorType.PARSER_SYMBOL] + ": c")


    def test_basic_4(self):
        with self.assertRaises(Exception) as exc:
            Parser(")4x(2x +1)").parse()
        error = exc.exception
        self.assertEqual(str(error), ErrorMessage[ErrorType.PARSER_BRACKET] + ": position 1")


    def test_negative_1(self):
        with self.assertRaises(Exception) as exc:
            Parser("(-*5 + x)").parse()
        error = exc.exception
        self.assertEqual(str(error), ErrorMessage[ErrorType.PARSER_NEGATIVE_SYMBOL])


    def test_negative_2(self):
        with self.assertRaises(Exception) as exc:
            Parser("5x * x-").parse()
        error = exc.exception
        self.assertEqual(str(error), ErrorMessage[ErrorType.PARSER_NEGATIVE_SYMBOL] + ": position: 7")

    def test_negative_3(self):
        with self.assertRaises(Exception) as exc:
            Parser("(5x + x)(5 + 3-)").parse()
        error = exc.exception
        self.assertEqual(str(error), ErrorMessage[ErrorType.PARSER_NEGATIVE_SYMBOL] + ": position: 15")


    def test_angle_bracket_1(self):
        with self.assertRaises(Exception) as exc:
            Parser("(5x + x)(<5> + <3)").parse()
        error = exc.exception
        self.assertEqual(str(error), ErrorMessage[ErrorType.PARSER_BRACKET_ANGLE])


    def test_angle_bracket_2(self):
        with self.assertRaises(Exception) as exc:
            Parser("(5x + x)(5 + 3>-)").parse()
        error = exc.exception
        self.assertEqual(str(error), ErrorMessage[ErrorType.PARSER_BRACKET_ANGLE] + ": position 15")


    def test_angle_bracket_3(self):
        with self.assertRaises(Exception) as exc:
            Parser("<(5x + x)(5 + 3)>>").parse()
        error = exc.exception
        self.assertEqual(str(error), ErrorMessage[ErrorType.PARSER_BRACKET_ANGLE] + ": position 18")


    def test_angle_bracket_4(self):
        with self.assertRaises(Exception) as exc:
            Parser("<(5x + x)(5 + 3)>").parse()
        error = exc.exception
        self.assertEqual(str(error), ErrorMessage[ErrorType.PARSER_BRACKET_ANGLE])


    def test_angle_bracket_5(self):
        with self.assertRaises(Exception) as exc:
            Parser("(5x + sqrt<>x)(5 + 3)").parse()
        error = exc.exception
        self.assertEqual(str(error), ErrorMessage[ErrorType.PARSER_BRACKET_ANGLE])


    def test_angle_bracket_6(self):
        with self.assertRaises(Exception) as exc:
            Parser("<>(5x)").parse()
        error = exc.exception
        self.assertEqual(str(error), ErrorMessage[ErrorType.PARSER_BRACKET_ANGLE])


    def test_angle_bracket_7(self):
        with self.assertRaises(Exception) as exc:
            Parser("5x + sin<4>x").parse()
        error = exc.exception
        self.assertEqual(str(error), ErrorMessage[ErrorType.PARSER_BRACKET_ANGLE])


