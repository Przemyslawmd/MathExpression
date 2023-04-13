
from collections import deque
from enum import Enum

import math
from numpy import power, arange

from tokens.token import TokenType
from tokens.tokenGroup import TokenGroup


class Direction(Enum):
    CONST = 0
    DOWN = 1
    UP = 2
    NONE = 3


actions = {
    TokenType.DIVISION: lambda a, b: math.nan if round(a, 4) == 0.00 else b / a,
    TokenType.MINUS: lambda a, b: b - a,
    TokenType.MULTIPLICATION: lambda a, b: a * b,
    TokenType.PLUS: lambda a, b: a + b,

    TokenType.LOG: lambda a, b: math.log(a, b) if a > 0 else math.nan,
    TokenType.POWER: lambda a, b: math.nan if (float(a).is_integer() is False and b < 0) else power(b, a),
    TokenType.ROOT: lambda a, b: math.nan if a < 0 else (math.sqrt(a) if b == 2 else power(a, 1 / b)),

    TokenType.COSINE: lambda a: math.cos(a),
    TokenType.COTANGENT: lambda a: math.nan if round(math.sin(a), 4) == 0.00 else math.cos(a) / math.sin(a),
    TokenType.SINE: lambda a: math.sin(a),
    TokenType.TANGENT: lambda a: math.tan(a),
}


class Calculator:

    @staticmethod
    def check_directions(numbers):
        directions = [Direction.NONE] * len(numbers)
        for index, number in enumerate(numbers):
            if index == 0:
                continue
            if math.isnan(number):
                directions[index] = Direction.NONE
            elif number > numbers[index - 1]:
                directions[index] = Direction.UP
            elif number < numbers[index - 1]:
                directions[index] = Direction.DOWN
            elif number == numbers[index - 1]:
                directions[index] = Direction.CONST
        return directions


    @staticmethod
    def is_discontinuity(directions, numbers, index):
        if directions[index - 1] == Direction.DOWN and directions[index] == Direction.UP:
            if directions[index + 1] == Direction.DOWN and numbers[index + 1] > numbers[index - 1]:
                return True
        if directions[index - 1] == Direction.UP and directions[index] == Direction.DOWN:
            if directions[index + 1] == Direction.UP and numbers[index + 1] < numbers[index - 1]:
                return True
        return False


    def check_continuity(self, numbers):
        discontinuity_points = []
        directions = self.check_directions(numbers)
        for index, direction in enumerate(directions):
            if index == 0:
                continue
            if direction != directions[index - 1]:
                if self.is_discontinuity(directions, numbers, index):
                    discontinuity_points.append(index)
        return discontinuity_points


    def calculate(self, postfix_tokens, min_x, max_x, x_precision=1.0):
        calculation_stack = deque()
        for _ in arange(min_x, max_x + x_precision, x_precision):
            calculation_stack.append(deque())

        for token in postfix_tokens:
            if token.type is TokenType.NUMBER:
                for calculation in calculation_stack:
                    calculation.append(token.data)
            elif token.type == TokenType.X:
                number = min_x
                for values in calculation_stack:
                    values.append(round(number, 4))
                    number += x_precision
            elif token.type is TokenType.X_NEGATIVE:
                number = min_x * -1.0
                for calculation in calculation_stack:
                    calculation.append(round(number, 4))
                    number -= x_precision
            elif token.type in TokenGroup.basic_arithmetic or token.type is TokenType.POWER:
                for calculation in calculation_stack:
                    num_1 = calculation.pop()
                    num_2 = calculation.pop()
                    calculation.append(actions[token.type](num_1, num_2))
            elif token.type in TokenGroup.trigonometry:
                for calculation in calculation_stack:
                    num = calculation.pop()
                    radian = math.radians(num)
                    calculation.append(actions[token.type](radian))
            elif token.type is TokenType.LOG or TokenType.ROOT:
                for calculation in calculation_stack:
                    num = calculation.pop()
                    calculation.append(actions[token.type](num, token.data))

        results = [round(x[0], 4) for x in calculation_stack]

        for token in postfix_tokens:
            discontinuity_points = []
            if token.type is TokenType.DIVISION:
                discontinuity_points = self.check_continuity(results)
                break
        for point in discontinuity_points:
            results[point] = math.nan

        return results


