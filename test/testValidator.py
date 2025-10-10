
from unittest import TestCase

from errors import Error, Message
from errorStorage import ErrorStorage
from tokens.parser import Parser


class TestParserError(TestCase):

    def tearDown(self):
        ErrorStorage.clear()


    def test_validator_bracket_empty_beginning(self):
        tokens = Parser("()").parse()
        errors = ErrorStorage.get_errors()
        self.assertIsNone(tokens)
        self.assertEqual(errors[0], Message[Error.VALIDATOR_BRACKET_LEFT])


    def test_validator_bracket_empty(self):
        tokens = Parser("5x + tg() + 34").parse()
        errors = ErrorStorage.get_errors()
        self.assertIsNone(tokens)
        self.assertEqual(errors[0], Message[Error.VALIDATOR_BRACKET_LEFT])


    def test_validator_arithmetic(self):
        tokens = Parser("5x + sin(x + )").parse()
        errors = ErrorStorage.get_errors()
        self.assertIsNone(tokens)
        self.assertEqual(errors[0], Message[Error.VALIDATOR_ARITHMETIC])


    def test_validator_invalid_last_symbol_1(self):
        tokens = Parser("5x + cosx +").parse()
        errors = ErrorStorage.get_errors()
        self.assertIsNone(tokens)
        self.assertEqual(errors[0], Message[Error.VALIDATOR_LAST_TOKEN])


    def test_validator_invalid_last_symbol_2(self):
        tokens = Parser("sin").parse()
        errors = ErrorStorage.get_errors()
        self.assertIsNone(tokens)
        self.assertEqual(errors[0], Message[Error.VALIDATOR_LAST_TOKEN])


    def test_validator_invalid_first_symbol_1(self):
        tokens = Parser("*12").parse()
        errors = ErrorStorage.get_errors()
        self.assertIsNone(tokens)
        self.assertEqual(errors[0], Message[Error.VALIDATOR_FIRST_TOKEN])


    def test_validator_invalid_first_symbol_2(self):
        tokens = Parser("/").parse()
        errors = ErrorStorage.get_errors()
        self.assertIsNone(tokens)
        self.assertEqual(errors[0], Message[Error.VALIDATOR_FIRST_TOKEN])


    def test_validator_logarithm_base_0(self):
        tokens = Parser("sinx + log<1>x").parse()
        errors = ErrorStorage.get_errors()
        self.assertIsNone(tokens)
        self.assertEqual(errors[0], Message[Error.VALIDATOR_LOGARITHM_BASE])


    def test_validator_logarithm_base_1(self):
        tokens = Parser("12x^2 - log<0>10").parse()
        errors = ErrorStorage.get_errors()
        self.assertIsNone(tokens)
        self.assertEqual(errors[0], Message[Error.VALIDATOR_LOGARITHM_BASE])


    def test_validator_root_degree(self):
        tokens = Parser("12x^2 - sqrt<0>10").parse()
        errors = ErrorStorage.get_errors()
        self.assertIsNone(tokens)
        self.assertEqual(errors[0], Message[Error.VALIDATOR_ROOT_DEGREE])

