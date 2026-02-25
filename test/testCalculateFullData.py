
import math
from numpy import arange
from unittest import TestCase

from postfix.calculator import calculate
from postfix.postfix import Postfix
from tree.tree import create_tree
from tokens.parser import Parser


class TestPostfixCalculateFullData(TestCase):

    @staticmethod
    def read_data_from_file(file_with_data):
        f = open("data/" + file_with_data, "r")
        data = f.read()
        f.close()
        return [float(x.strip()) for x in data.split(',')]


    def run_test(self, expression, x_min, x_max, precision, file_result):
        tokens = Parser(expression).parse()
        postfix = Postfix().create_postfix(tokens)
        root = create_tree(postfix)
        x_values = arange(x_min, x_max, precision)
        y_calculated = [round(x, 4) for x in calculate(root, x_values)]
        y_expected = self.read_data_from_file(file_result)
        for y_cal, y_exp in zip(y_calculated, y_expected):
            if math.isnan(y_cal):
                assert math.isnan(y_exp)
                continue
            assert y_cal == y_exp


    def test_postfix_calculate_full_data_1(self):
        self.run_test("x^3 (x - 1)(x - 2)^2", -3, 3.1, 0.1, "resultsA")


    def test_postfix_calculate_full_data_2(self):
        self.run_test("(x^2 -3)/(x - 2)", -20, 20.05, 0.05, "resultsB")


    def test_postfix_calculate_full_data_3(self):
        self.run_test("sqrt((1-x)/(1+x))", -6, 5.02, 0.02, "resultsC")


    def test_postfix_calculate_full_data_4(self):
        self.run_test("(sinx)^2 + cosx", -360, 360.02, 0.2, "resultsD")


    def test_postfix_calculate_full_data_5(self):
        self.run_test("x^2 (x^2 -4)^3", -3, 3.01, 0.01, "resultsE")


    def test_postfix_calculate_full_data_6(self):
        self.run_test("(15x^2 - 13x -20)/(8x^2 + 10x -7)", -10, 10.01, 0.01, "resultsF")

