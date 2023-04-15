
import math
from unittest import TestCase

from postfix.calculator import Calculator
from postfix.postfix import Postfix
from tokens.parser import Parser


class TestPostfixCalculateFullData(TestCase):

    @staticmethod
    def read_data_from_file(file_with_data):
        f = open(file_with_data, "r")
        data = f.read()
        f.close()
        return [float(x.strip()) for x in data.split(',')]


    def test_postfix_calculate_full_data_1(self):
        tokens = Parser("x^3 (x - 1)(x - 2)^2").parse()
        postfix = Postfix().create_postfix(tokens)
        result = Calculator().calculate(postfix, -3, 3, 0.1)
        file_result = self.read_data_from_file("data/resultsA")
        self.assertListEqual(file_result, result)


    def test_postfix_calculate_full_data_2(self):
        tokens = Parser("(x^2 -3)/(x - 2)").parse()
        postfix = Postfix().create_postfix(tokens)
        result = Calculator().calculate(postfix, -20, 20, 0.05)
        file_result = self.read_data_from_file("data/resultsB")
        for x, y in zip(result, file_result):
            if math.isnan(x):
                assert math.isnan(y)
                continue
            assert x == y


    def test_postfix_calculate_full_data_3(self):
        tokens = Parser("sqrt((1-x)/(1+x))").parse()
        postfix = Postfix().create_postfix(tokens)
        result = Calculator().calculate(postfix, -6, 5, 0.02)
        file_result = self.read_data_from_file("data/resultsC")
        for x, y in zip(result, file_result):
            if math.isnan(x):
                assert math.isnan(y)
                continue
            assert x == y


    def test_postfix_calculate_full_data_4(self):
        tokens = Parser("(sinx)^2 + cosx").parse()
        postfix = Postfix().create_postfix(tokens)
        result = Calculator().calculate(postfix, -360, 360, 0.2)
        file_result = self.read_data_from_file("data/resultsD")
        self.assertListEqual(file_result, result)


    def test_postfix_calculate_full_data_5(self):
        tokens = Parser("x^2 (x^2 -4)^3").parse()
        postfix = Postfix().create_postfix(tokens)
        result = Calculator().calculate(postfix, -3, 3, 0.01)
        file_result = self.read_data_from_file("data/resultsE")
        self.assertListEqual(file_result, result)


    def test_postfix_calculate_full_data_6(self):
        tokens = Parser("(15x^2 - 13x -20)/(8x^2 + 10x -7)").parse()
        postfix = Postfix().create_postfix(tokens)
        result = Calculator().calculate(postfix, -10, 10, 0.01)
        file_result = self.read_data_from_file("data/resultsF")
        for x, y in zip(result, file_result):
            if math.isnan(x):
                assert math.isnan(y)
                continue
            assert x == y


