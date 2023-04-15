
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
        [print(f"{r.expression}; action: {r.action}; range: {r.min}:{r.max}; precision: {r.precision}; time: {r.time}")
         for r in self.results]


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


