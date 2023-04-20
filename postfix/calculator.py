
from collections import deque
from enum import Enum

from math import cos, isnan, log, nan, radians, sin, sqrt, tan
from numpy import power, arange

from tokens.token import TokenType
from tokens.tokenGroup import TokenGroup


class Direction(Enum):
    CONST = 0
    DOWN = 1
    UP = 2
    NONE = 3


actions = {
    TokenType.DIVISION: lambda a, b: nan if round(a, 4) == 0.00 else b / a,
    TokenType.MINUS: lambda a, b: b - a,
    TokenType.MULTIPLICATION: lambda a, b: a * b,
    TokenType.PLUS: lambda a, b: a + b,

    TokenType.LOG: lambda a, b: log(a, b) if a > 0 else nan,
    TokenType.POWER: lambda a, b: nan if (float(a).is_integer() is False and b < 0) else power(b, a),
    TokenType.ROOT: lambda a, b: nan if a < 0 else (sqrt(a) if b == 2 else power(a, 1 / b)),

    TokenType.COSINE: lambda a: cos(a),
    TokenType.COTANGENT: lambda a: nan if round(sin(a), 4) == 0.00 else cos(a) / sin(a),
    TokenType.SINE: lambda a: sin(a),
    TokenType.TANGENT: lambda a: tan(a),
}


def check_directions(numbers):
    directions = [Direction.NONE] * len(numbers)
    for index, number in enumerate(numbers):
        if index == 0:
            continue
        if isnan(number):
            directions[index] = Direction.NONE
        elif number > numbers[index - 1]:
            directions[index] = Direction.UP
        elif number < numbers[index - 1]:
            directions[index] = Direction.DOWN
        elif number == numbers[index - 1]:
            directions[index] = Direction.CONST
    return directions


def is_discontinuity(directions, numbers, index):
    if directions[index - 1] == Direction.DOWN and directions[index] == Direction.UP:
        if directions[index + 1] == Direction.DOWN and numbers[index + 1] > numbers[index - 1]:
            return True
    if directions[index - 1] == Direction.UP and directions[index] == Direction.DOWN:
        if directions[index + 1] == Direction.UP and numbers[index + 1] < numbers[index - 1]:
            return True
    return False


def check_continuity(numbers):
    discontinuity_points = []
    directions = check_directions(numbers)
    for index, direction in enumerate(directions[1:]):
        if direction != directions[index - 1]:
            if is_discontinuity(directions, numbers, index):
                discontinuity_points.append(index)
    return discontinuity_points


def calculate(tokens, min_x, max_x, precision=1.0):
    calculation_stacks = []
    x_values = arange(min_x, max_x + precision, precision)
    [calculation_stacks.append(deque()) for _ in x_values]

    for token in tokens:
        if token.type is TokenType.NUMBER:
            [calc.append(token.data) for calc in calculation_stacks]
        elif token.type is TokenType.X:
            [calculation_stacks[i].append(x) for i, x in enumerate(x_values)]
        elif token.type is TokenType.X_NEGATIVE:
            [calculation_stacks[i].append(x * -1.0) for i, x in enumerate(x_values)]
        elif token.type in TokenGroup.basic_arithmetic or token.type is TokenType.POWER:
            for calc in calculation_stacks:
                num_1 = calc.pop()
                num_2 = calc.pop()
                calc.append(actions[token.type](num_1, num_2))
        elif token.type in TokenGroup.trigonometry:
            for calc in calculation_stacks:
                num = calc.pop()
                radian = radians(num)
                calc.append(actions[token.type](radian))
        elif token.type is TokenType.LOG or TokenType.ROOT:
            for calc in calculation_stacks:
                num = calc.pop()
                calc.append(actions[token.type](num, token.data))

    results = [round(x[0], 4) for x in calculation_stacks]

    if [token for token in tokens if token.type in (TokenType.DIVISION, TokenType.TANGENT)]:
        discontinuity_points = check_continuity(results)
        for point in discontinuity_points:
            results[point] = nan

    return results


