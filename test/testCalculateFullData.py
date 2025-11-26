
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


    def test_postfix_calculate_full_data_1(self):
        tokens = Parser("x^3 (x - 1)(x - 2)^2").parse()
        postfix = Postfix().create_postfix(tokens)
        root = create_tree(postfix)
        x_values = arange(-3, 3.1, 0.1)
        result = calculate(root, x_values)
        file_result = self.read_data_from_file("resultsA")
        self.assertListEqual(file_result, result)


    def test_postfix_calculate_full_data_2(self):
        tokens = Parser("(x^2 -3)/(x - 2)").parse()
        postfix = Postfix().create_postfix(tokens)
        root = create_tree(postfix)
        x_values = arange(-20, 20.05, 0.05)
        result = calculate(root, x_values)
        file_result = self.read_data_from_file("resultsB")
        for x, y in zip(result, file_result):
            if math.isnan(x):
                assert math.isnan(y)
                continue
            assert x == y


    def test_postfix_calculate_full_data_3(self):
        tokens = Parser("sqrt((1-x)/(1+x))").parse()
        postfix = Postfix().create_postfix(tokens)
        root = create_tree(postfix)
        x_values = arange(-6, 5.02, 0.02)
        result = calculate(root, x_values)
        file_result = self.read_data_from_file("resultsC")
        for x, y in zip(result, file_result):
            if math.isnan(x):
                assert math.isnan(y)
                continue
            assert x == y


    def test_postfix_calculate_full_data_4(self):
        tokens = Parser("(sinx)^2 + cosx").parse()
        postfix = Postfix().create_postfix(tokens)
        root = create_tree(postfix)
        x_values = arange(-360, 360.2, 0.2)
        result = calculate(root, x_values)
        file_result = self.read_data_from_file("resultsD")
        self.assertListEqual(file_result, result)


    def test_postfix_calculate_full_data_5(self):
        tokens = Parser("x^2 (x^2 -4)^3").parse()
        postfix = Postfix().create_postfix(tokens)
        root = create_tree(postfix)
        x_values = arange(-3, 3.01, 0.01)
        result = calculate(root, x_values)
        file_result = self.read_data_from_file("resultsE")
        self.assertListEqual(file_result, result)


    def test_postfix_calculate_full_data_6(self):
        tokens = Parser("(15x^2 - 13x -20)/(8x^2 + 10x -7)").parse()
        postfix = Postfix().create_postfix(tokens)
        root = create_tree(postfix)
        x_values = arange(-10, 10.01, 0.01)
        result = calculate(root, x_values)
        file_result = self.read_data_from_file("resultsF")
        for x, y in zip(result, file_result):
            if math.isnan(x):
                assert math.isnan(y)
                continue
            assert x == y


