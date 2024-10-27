from timeit import default_timer
from collections import namedtuple
from datetime import datetime
from unittest import TestCase

from postfix.calculator import calculate
from postfix.postfix import Postfix
from tokens.parser import Parser

Result = namedtuple('Result', ('expression', 'action', 'min', 'max', 'precision', 'time'))


class TestPerformance(TestCase):
    results = []

    def test_performance(self):
        self.calculation_1(5)
        self.calculation_2(5)
        self.calculation_3(5)
        self.calculation_4(5)
        self.postfix_parser_1(5)
        self.postfix_parser_2(5)
        self.postfix_parser_3(5)
        self.postfix_parser_4(5)

        file = open("performanceResults.txt", "a")
        file.write(f"{datetime.now()}\n\n")
        [file.write(f"{r.expression:<64} "
                    f"action: {r.action:<14} "
                    f"range: {r.min}:{r.max:<5} "
                    f"precision: {r.precision:<7} "
                    f"time: {r.time}\n") for r in self.results]
        file.write("\n\n")

    def calculation_1(self, count):
        expression = "x^2 + 2(sinx + cosx)"
        tokens = Parser(expression).parse()
        postfix = Postfix().create_postfix(tokens)
        for _ in range(count):
            start = default_timer()
            calculate(postfix, -360, 360, 0.01)
            end = default_timer()
            self.results.append(Result(expression, "calculation", -360, 360, 0.01, end - start))

    def calculation_2(self, count):
        expression = "sqrtx + logx - 2(sinx + 3)^2"
        tokens = Parser(expression).parse()
        postfix = Postfix().create_postfix(tokens)
        for _ in range(count):
            start = default_timer()
            calculate(postfix, -500, 500, 0.05)
            end = default_timer()
            self.results.append(Result(expression, "calculation", -500, 500, 0.05, end - start))

    def calculation_3(self, count):
        expression = "x^4 + 2x^2 + (x + 3)^3"
        tokens = Parser(expression).parse()
        postfix = Postfix().create_postfix(tokens)
        for _ in range(count):
            start = default_timer()
            calculate(postfix, -500, 500, 0.01)
            end = default_timer()
            self.results.append(Result(expression, "calculation", -500, 500, 0.01, end - start))

    def calculation_4(self, count):
        expression = "(x + sinx)^2 + (cosx - 100)(sinx + 200) + (sinx + cosx) / 100"
        tokens = Parser(expression).parse()
        postfix = Postfix().create_postfix(tokens)
        for _ in range(count):
            start = default_timer()
            calculate(postfix, -500, 500, 0.01)
            end = default_timer()
            self.results.append(Result(expression, "calculation", -500, 500, 0.01, end - start))

    def postfix_parser_1(self, count):
        for _ in range(count):
            expression = "x^2 + 2(sinx + cosx)"
            start = default_timer()
            Parser(expression).parse()
            end = default_timer()
            self.results.append(Result(expression, "parser", 0, 0, 0, end - start))

    def postfix_parser_2(self, count):
        for _ in range(count):
            expression = "sqrtx + logx - 2(sinx + 3)^2"
            start = default_timer()
            Parser(expression).parse()
            end = default_timer()
            self.results.append(Result(expression, "parser", 0, 0, 0, end - start))

    def postfix_parser_3(self, count):
        for _ in range(count):
            expression = "x^4 + 2x^2 + (x + 3)^3"
            start = default_timer()
            Parser(expression).parse()
            end = default_timer()
            self.results.append(Result(expression, "parser", 0, 0, 0, end - start))

    def postfix_parser_4(self, count):
        for _ in range(count):
            expression = "(x + sinx)^2 + (cosx - 100)(sinx + 200) + (sinx + cosx) / 100"
            start = default_timer()
            Parser(expression).parse()
            end = default_timer()
            self.results.append(Result(expression, "parser", 0, 0, 0, end - start))
