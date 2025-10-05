
from unittest import TestCase

from errors import Error, Message
from errorStorage import ErrorStorage
from tokens.parser import Parser


class TestParserError(TestCase):

    def tearDown(self):
        ErrorStorage.clear()


    def test_validator_bracket_empty_beginning(self):
        Parser("()").parse()
        errors = ErrorStorage.get_errors()
        self.assertEqual(errors[0], Message[Error.VALIDATOR_BRACKET_LEFT])


    def test_validator_bracket_empty(self):
        Parser("5x + tg() + 34").parse()
        errors = ErrorStorage.get_errors()
        self.assertEqual(errors[0], Message[Error.VALIDATOR_BRACKET_LEFT])


    def test_validator_arithmetic(self):
        Parser("5x + sin(x + )").parse()
        errors = ErrorStorage.get_errors()
        self.assertEqual(errors[0], Message[Error.VALIDATOR_ARITHMETIC])


    def test_validator_invalid_last_symbol_1(self):
        Parser("5x + cosx +").parse()
        errors = ErrorStorage.get_errors()
        self.assertEqual(errors[0], Message[Error.VALIDATOR_LAST_TOKEN])


    def test_validator_invalid_last_symbol_2(self):
        Parser("sin").parse()
        errors = ErrorStorage.get_errors()
        self.assertEqual(errors[0], Message[Error.VALIDATOR_LAST_TOKEN])


    def test_validator_invalid_first_symbol_1(self):
        Parser("*12").parse()
        errors = ErrorStorage.get_errors()
        self.assertEqual(errors[0], Message[Error.VALIDATOR_FIRST_TOKEN])


    def test_validator_invalid_first_symbol_2(self):
        Parser("/").parse()
        errors = ErrorStorage.get_errors()
        self.assertEqual(errors[0], Message[Error.VALIDATOR_FIRST_TOKEN])

