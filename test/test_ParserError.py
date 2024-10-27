
from unittest import TestCase

from errors import Error, ErrorMessage
from errorStorage import ErrorStorage
from tokens.parser import Parser


class TestParserError(TestCase):

    def test_basic_1(self):
        Parser("(2x + 3) / ((3x + 4)").parse()
        error = ErrorStorage.getErrors()[0]
        self.assertEqual(str(error), ErrorMessage[Error.PARSER_BRACKET])


    def test_basic_2(self):
        Parser("12y + 4").parse()
        error = ErrorStorage.getErrors()[0]
        self.assertEqual(str(error), ErrorMessage[Error.PARSER_SYMBOL] + ": y")


    def test_basic_3(self):
        Parser("tg45 * cor30 - 3").parse()
        error = ErrorStorage.getErrors()[0]
        self.assertEqual(str(error), ErrorMessage[Error.PARSER_SYMBOL] + ": c")


    def test_basic_4(self):
        Parser(")4x(2x +1)").parse()
        error = ErrorStorage.getErrors()[0]
        self.assertEqual(str(error), ErrorMessage[Error.PARSER_BRACKET])


    def test_negative_1(self):
        Parser("(-*5 + x)").parse()
        error = ErrorStorage.getErrors()[0]
        self.assertEqual(str(error), ErrorMessage[Error.PARSER_NEGATIVE_SYMBOL])


    def test_negative_2(self):
        Parser("5x * x-").parse()
        error = ErrorStorage.getErrors()[0]
        self.assertEqual(str(error), ErrorMessage[Error.PARSER_NEGATIVE_SYMBOL])


    def test_negative_3(self):
        Parser("(5x + x)(5 + 3-)").parse()
        error = ErrorStorage.getErrors()[0]
        self.assertEqual(str(error), ErrorMessage[Error.PARSER_NEGATIVE_SYMBOL])


    def test_negative_4(self):
        Parser("(5x + x)(5 + 3>-)").parse()
        error = ErrorStorage.getErrors()[0]
        self.assertEqual(str(error), ErrorMessage[Error.PARSER_NEGATIVE_SYMBOL])


    def test_angle_bracket_1(self):
        Parser("(5x + x)(<5> + <3)").parse()
        error = ErrorStorage.getErrors()[0]
        self.assertEqual(str(error), ErrorMessage[Error.PARSER_BRACKET_ANGLE])


    def test_angle_bracket_2(self):
        Parser("<(5x + x)(5 + 3)>>").parse()
        error = ErrorStorage.getErrors()[0]
        self.assertEqual(str(error), ErrorMessage[Error.PARSER_BRACKET_ANGLE])


    def test_angle_bracket_3(self):
        Parser("<(5x + x)(5 + 3)>").parse()
        error = ErrorStorage.getErrors()[0]
        self.assertEqual(str(error), ErrorMessage[Error.PARSER_BRACKET_ANGLE])


    def test_angle_bracket_4(self):
        Parser("(5x + sqrt<>x)(5 + 3)").parse()
        error = ErrorStorage.getErrors()[0]
        self.assertEqual(str(error), ErrorMessage[Error.PARSER_BRACKET_ANGLE])


    def test_angle_bracket_5(self):
        Parser("<>(5x)").parse()
        error = ErrorStorage.getErrors()[0]
        self.assertEqual(str(error), ErrorMessage[Error.PARSER_BRACKET_ANGLE])


    def test_angle_bracket_6(self):
        Parser("5x + sin<4>x").parse()
        error = ErrorStorage.getErrors()[0]
        self.assertEqual(str(error), ErrorMessage[Error.PARSER_BRACKET_ANGLE])


