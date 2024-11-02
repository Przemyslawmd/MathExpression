
from collections import deque
from enum import Enum

from math import cos, log, nan, radians, sin, sqrt, tan
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
        elif number > numbers[index - 1]:
            directions[index] = Direction.UP
        elif number < numbers[index - 1]:
            directions[index] = Direction.DOWN
        elif number == numbers[index - 1]:
            directions[index] = Direction.CONST
    return directions


def is_discontinuity(directions, numbers, index):
    direction_prev = directions[index - 1]
    direction_curr = directions[index]
    number_prev = numbers[index - 1]
    number_curr = numbers[index]
    if all((direction_prev == Direction.UP, direction_curr == Direction.DOWN, number_prev > 0, number_curr < 0)):
        return True
    if all((direction_prev == Direction.DOWN, direction_curr == Direction.UP, number_prev < 0, number_curr > 0)):
        return True
    return False


def check_continuity(numbers):
    discontinuity_points = []
    directions = check_directions(numbers)
    for index, direction in enumerate(directions):
        if direction != directions[index - 1]:
            if is_discontinuity(directions, numbers, index):
                discontinuity_points.append(index)
    return discontinuity_points


def calculate(tokens, min_x, max_x, precision=1.0):
    calc_stacks = []
    x_values = arange(min_x, max_x + precision, precision)
    for _ in x_values:
        calc_stacks.append(deque())

    for token in tokens:
        if token.type is TokenType.NUMBER:
            for calc in calc_stacks:
                calc.append(token.data)
        elif token.type is TokenType.X:
            for calc, x in zip(calc_stacks, x_values):
                calc.append(x)
        elif token.type is TokenType.X_NEGATIVE:
            for calc, x in zip(calc_stacks, x_values):
                calc.append(x * -1.0)
        elif token.type in TokenGroup.arithmetic or token.type is TokenType.POWER:
            for calc in calc_stacks:
                num_1 = calc.pop()
                num_2 = calc.pop()
                calc.append(actions[token.type](num_1, num_2))
        elif token.type in TokenGroup.trigonometry:
            for calc in calc_stacks:
                num = calc.pop()
                radian = radians(num)
                calc.append(actions[token.type](radian))
        elif token.type is TokenType.LOG or TokenType.ROOT:
            for calc in calc_stacks:
                num = calc.pop()
                calc.append(actions[token.type](num, token.data))

    results = [round(x[0], 4) for x in calc_stacks]

    if [token for token in tokens if token.type in (TokenType.DIVISION, TokenType.TANGENT)]:
        discontinuity_points = check_continuity(results)
        for point in discontinuity_points:
            results[point] = nan

    return results


