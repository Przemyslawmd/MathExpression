
from unittest import TestCase

from errors import Error, ErrorMessage
from errorStorage import ErrorStorage
from tokens.parser import Parser


class TestParserError(TestCase):

    def tearDown(self):
        ErrorStorage.clear()


    def test_validator_bracket_empty_beginning(self):
        Parser("()").parse()
        errors = ErrorStorage.get_errors()
        self.assertEqual(errors[0], ErrorMessage[Error.VALIDATOR_BRACKET_LEFT])


    def test_validator_bracket_empty(self):
        Parser("5x + tg() + 34").parse()
        errors = ErrorStorage.get_errors()
        self.assertEqual(errors[0], ErrorMessage[Error.VALIDATOR_BRACKET_LEFT])


    def test_validator_arithmetic(self):
        Parser("5x + sin(x + )").parse()
        errors = ErrorStorage.get_errors()
        self.assertEqual(errors[0], ErrorMessage[Error.VALIDATOR_ARITHMETIC])


