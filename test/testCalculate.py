
from math import isclose
from unittest import TestCase

from controller import calculate_values
from postfix.calculator import calculate
from postfix.postfix import Postfix
from tokens.parser import Parser
from postfix.tree import create_tree


class TestCalculate(TestCase):

    def test_fill_x(self):
        step = 0.5
        result = calculate_values("x", 20, 30, step)
        assert len(result) == 21
        shift = 0
        for value in result:
            assert value == 20 + shift
            shift += step


    def test_fill_x_brackets_1(self):
        step = 0.5
        result = calculate_values("(x)", -30, 20, step)
        assert len(result) == 101
        shift = 0
        for value in result:
            assert value == -30 + shift
            shift += step


    def test_fill_x_brackets_2(self):
        step = 0.1
        result = calculate_values("(((x)))", 2, 5, step)
        assert len(result) == 31
        shift = 0
        for value in result:
            assert isclose(value, 2 + shift)
            shift += step


    def test_fill_negative_x(self):
        step = 0.5
        result = calculate_values("-x", 20, 30, step)
        assert len(result) == 21
        shift = 0
        for value in result:
            assert value == 20 * -1 - shift
            shift += step


    def test_fill_number(self):
        result = calculate_values("10", -5, 5, 1)
        assert len(result) == 11
        for value in result:
            assert value == 10


    def test_fill_number_brackets(self):
        result = calculate_values("(100)", -5, 5, 1)
        assert len(result) == 11
        for value in result:
            assert value == 100


    def test_calculate_1(self):
        tokens = Parser("3 + x * 10 + x").parse()
        postfix = Postfix().create_postfix(tokens)
        root = create_tree(postfix)
        result = calculate(root, 2, 3)
        assert result[0] == 25
        assert result[1] == 36


    def test_calculate_2(self):
        tokens = Parser("2(x + 5)").parse()
        postfix = Postfix().create_postfix(tokens)
        root = create_tree(postfix)
        result = calculate(root, 2, 3)
        assert result[0] == 14
        assert result[1] == 16


    def test_calculate_3(self):
        tokens = Parser("(3 + x) * (10 + x)").parse()
        postfix = Postfix().create_postfix(tokens)
        root = create_tree(postfix)
        result = calculate(root, 5, 6)
        assert result[0] == 120
        assert result[1] == 144


    def test_calculate_4(self):
        tokens = Parser("2 * (3 + x) * 4").parse()
        postfix = Postfix().create_postfix(tokens)
        root = create_tree(postfix)
        result = calculate(root, 2, 5)
        assert result[0] == 40
        assert result[1] == 48
        assert result[2] == 56
        assert result[3] == 64


    def test_calculate_5(self):
        tokens = Parser("(4x + x3)2x").parse()
        postfix = Postfix().create_postfix(tokens)
        root = create_tree(postfix)
        result = calculate(root, 0, 5)
        assert result[0] == 0
        assert result[1] == 14
        assert result[2] == 56
        assert result[3] == 126
        assert result[4] == 224
        assert result[5] == 350


    def test_calculate_6(self):
        tokens = Parser("(2 - x3)4").parse()
        postfix = Postfix().create_postfix(tokens)
        root = create_tree(postfix)
        result = calculate(root, 10, 12)
        assert result[0] == -112
        assert result[1] == -124
        assert result[2] == -136


    def test_calculate_7(self):
        tokens = Parser("(-x - 3)4").parse()
        postfix = Postfix().create_postfix(tokens)
        root = create_tree(postfix)
        result = calculate(root, 5, 7)
        assert result[0] == -32
        assert result[1] == -36
        assert result[2] == -40


    def test_calculate_8(self):
        tokens = Parser("(x +3)(-5)").parse()
        postfix = Postfix().create_postfix(tokens)
        root = create_tree(postfix)
        result = calculate(root, 100, 103)
        assert result[0] == -515
        assert result[1] == -520
        assert result[2] == -525
        assert result[3] == -530


    def test_calculate_9(self):
        tokens = Parser("(-x -2)(-7)").parse()
        postfix = Postfix().create_postfix(tokens)
        root = create_tree(postfix)
        result = calculate(root, -2, 2)
        assert result[0] == 0
        assert result[1] == 7
        assert result[2] == 14
        assert result[3] == 21
        assert result[4] == 28


    def test_calculate_10(self):
        tokens = Parser("sinx + x").parse()
        postfix = Postfix().create_postfix(tokens)
        root = create_tree(postfix)
        result = calculate(root, 30, 30)
        assert result[0] == 30.5


    def test_calculate_11(self):
        tokens = Parser("xcos10").parse()
        postfix = Postfix().create_postfix(tokens)
        root = create_tree(postfix)
        result = calculate(root, 10, 14)
        assert result[0] == 9.8481
        assert result[1] == 10.8329
        assert result[2] == 11.8177
        assert result[3] == 12.8025
        assert result[4] == 13.7873


    def test_calculate_12(self):
        tokens = Parser("10tgx - xctgx").parse()
        postfix = Postfix().create_postfix(tokens)
        root = create_tree(postfix)
        result = calculate(root, 100, 104)
        assert result[0] == -39.0801
        assert result[1] == -31.8131
        assert result[2] == -25.3655
        assert result[3] == -19.5353
        assert result[4] == -14.1777


    def test_calculate_13(self):
        tokens = Parser("sqrtx + 10").parse()
        postfix = Postfix().create_postfix(tokens)
        root = create_tree(postfix)
        result = calculate(root, 16, 20)
        assert result[0] == 14.0
        assert result[1] == 14.1231
        assert result[2] == 14.2426
        assert result[3] == 14.3589
        assert result[4] == 14.4721


    def test_calculate_14(self):
        tokens = Parser("x + 2sqrt4").parse()
        postfix = Postfix().create_postfix(tokens)
        root = create_tree(postfix)
        result = calculate(root, 10, 15)
        assert result[0] == 14
        assert result[1] == 15
        assert result[2] == 16
        assert result[3] == 17
        assert result[4] == 18


    def test_calculate_15(self):
        tokens = Parser("xsqrt<3>8").parse()
        postfix = Postfix().create_postfix(tokens)
        root = create_tree(postfix)
        result = calculate(root, -10, -8)
        assert result[0] == -20
        assert result[1] == -18
        assert result[2] == -16


    def test_calculate_16(self):
        tokens = Parser("xsqrt(sinx)").parse()
        postfix = Postfix().create_postfix(tokens)
        root = create_tree(postfix)
        result = calculate(root, 30, 35)
        assert result[0] == 21.2132
        assert result[1] == 22.2475
        assert result[2] == 23.2946
        assert result[3] == 24.3539
        assert result[4] == 25.4249
        assert result[5] == 26.5072
