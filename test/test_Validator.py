
from unittest import TestCase

from errors import Error, ErrorMessage
from errorStorage import ErrorStorage
from tokens.parser import Parser


class TestParserError(TestCase):

    def tearDown(self):
        ErrorStorage.clear()

    def test_parser_bracket_6(self):
        Parser("5x + tg() + 34").parse()
        errors = ErrorStorage.get_errors()
        self.assertEqual(errors[0], ErrorMessage[Error.VALIDATOR_BRACKET_LEFT])

