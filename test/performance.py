
from timeit import default_timer
from collections import namedtuple
from unittest import TestCase

from postfix.calculator import calculate
from postfix.postfix import Postfix
from tokens.parser import Parser

Result = namedtuple('Result', ('expression', 'action', 'min', 'max', 'precision', 'time'))


class TestPerformance(TestCase):

    results = []

    def test_performance(self):
        self.performance_1(5)
        self.performance_2(5)
        self.performance_3(5)
        self.performance_4(5)
        [print(f"{r.expression:<64} "
               f"action: {r.action:<14} "
               f"range: {r.min}:{r.max:<5} "
               f"precision: {r.precision:<7} "
               f"time: {r.time}") for r in self.results]


    def performance_1(self, count):
        expression = "x^2 + 2(sinx + cosx)"
        tokens = Parser(expression).parse()
        postfix = Postfix().create_postfix(tokens)
        for _ in range(count):
            start = default_timer()
            calculate(postfix, -360, 360, 0.01)
            end = default_timer()
            self.results.append(Result(expression, "calculation", -360, 360, 0.01, end - start))


    def performance_2(self, count):
        expression = "sqrtx + logx - 2(sinx + 3)^2"
        tokens = Parser(expression).parse()
        postfix = Postfix().create_postfix(tokens)
        for _ in range(count):
            start = default_timer()
            calculate(postfix, -500, 500, 0.05)
            end = default_timer()
            self.results.append(Result(expression, "calculation", -500, 500, 0.05, end - start))


    def performance_3(self, count):
        expression = "x^4 + 2x^2 + (x + 3)^3"
        tokens = Parser(expression).parse()
        postfix = Postfix().create_postfix(tokens)
        for _ in range(count):
            start = default_timer()
            calculate(postfix, -500, 500, 0.01)
            end = default_timer()
            self.results.append(Result(expression, "calculation", -500, 500, 0.01, end - start))


    def performance_4(self, count):
        expression = "(x + sinx)^2 + (cosx - 100)(sinx + 200) + (sinx + cosx) / 100"
        tokens = Parser(expression).parse()
        postfix = Postfix().create_postfix(tokens)
        for _ in range(count):
            start = default_timer()
            calculate(postfix, -500, 500, 0.01)
            end = default_timer()
            self.results.append(Result(expression, "calculation", -500, 500, 0.01, end - start))


