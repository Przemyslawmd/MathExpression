import math
from unittest import TestCase
from Notations.Postfix import Postfix
from Tokens.Parser import Parser


class TestPostfixCalculateFullData(TestCase):

    @staticmethod
    def read_data_from_file(file_with_data):
        f = open(file_with_data, "r")
        data = f.read()
        f.close()
        return [float(x.strip()) for x in data.split(',')]


    def test_postfix_calculate_full_data_1(self):
        tokens = Parser("x^3 (x - 1)(x - 2)^2").parse()
        postfix = Postfix()
        postfix.create_postfix(tokens)
        result = postfix.calculate(-3, 3, 0.1)
        file_result = self.read_data_from_file("Data/resultsA")
        self.assertListEqual(file_result, result)


    def test_postfix_calculate_full_data_2(self):
        tokens = Parser("(x^2 -3)/(x - 2)").parse()
        postfix = Postfix()
        postfix.create_postfix(tokens)
        result = postfix.calculate(-20, 20, 0.05)
        file_result = self.read_data_from_file("Data/resultsB")
        for x, y in zip(result, file_result):
            if math.isnan(x):
                assert math.isnan(y)
                continue
            assert x == y


