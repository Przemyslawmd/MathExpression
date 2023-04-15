
from timeit import default_timer

from unittest import TestCase

from postfix.calculator import calculate
from postfix.postfix import Postfix
from tokens.parser import Parser


class TestPerformance(TestCase):

    def test_check_performance_1(self):
        tokens = Parser("x^2 + 2(sinx + cosx)").parse()
        postfix = Postfix().create_postfix(tokens)
        for _ in range(5):
            start = default_timer()
            calculate(postfix, -360, 360, 0.01)
            end = default_timer()
            print(f"Time: {end - start}")
