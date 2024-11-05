
from collections import deque
from enum import Enum

from math import cos, log, nan, radians, sin, sqrt, tan
from numpy import power, arange

from tokens.token import TokenType
from tokens.tokenGroup import TokenGroup

from collections import namedtuple


class Direction(Enum):
    CONST = 0
    DOWN = 1
    UP = 2
    NONE = 3


FunctionArg = {'X': 0, 'X_NEGATIVE': 1, 'RESULT': 2}


Action = namedtuple('Action', ('function', 'num_of_args', 'arg_1', 'arg_2'))


actions = {
    TokenType.DIVISION: lambda a, b: nan if round(a, 4) == 0.00 else b / a,
    TokenType.MINUS: lambda a, b: b - a,
    TokenType.MULTIPLICATION: lambda a, b: a * b,
    TokenType.PLUS: lambda a, b: a + b,

    TokenType.LOG: lambda a, b: log(a, b) if a > 0 else nan,
    TokenType.POWER: lambda a, b: nan if (float(a).is_integer() is False and b < 0) else power(b, a),
    TokenType.ROOT: lambda a, b: nan if a < 0 else (sqrt(a) if b == 2 else power(a, 1 / b)),

    TokenType.COSINE: lambda a: cos(radians(a)),
    TokenType.COTANGENT: lambda a: nan if round(sin(radians(a)), 4) == 0.00 else cos(radians(a)) / sin(radians(a)),
    TokenType.SINE: lambda a: sin(radians(a)),
    TokenType.TANGENT: lambda a: tan(radians(a)),
}


def check_directions(numbers) -> list:
    directions = [Direction.NONE] * len(numbers)
    for index, number in enumerate(numbers):
        if index == 0:
            continue
        elif number > numbers[index - 1]:
            directions[index] = Direction.UP
        elif number < numbers[index - 1]:
            directions[index] = Direction.DOWN
        else:
            directions[index] = Direction.CONST
    return directions


def is_discontinuity(direction_prev, direction_curr, number_prev, number_curr) -> bool:
    if all((direction_prev is Direction.UP, direction_curr is Direction.DOWN, number_prev > 0, number_curr < 0)):
        return True
    if all((direction_prev is Direction.DOWN, direction_curr is Direction.UP, number_prev < 0, number_curr > 0)):
        return True
    return False


def check_continuity(numbers) -> list:
    directions = check_directions(numbers)
    discontinuity_points = []
    for index, direction in enumerate(directions):
        if direction != directions[index - 1]:
            if is_discontinuity(directions[index - 1], direction, numbers[index - 1], numbers[index]):
                discontinuity_points.append(index)
    return discontinuity_points


def check_function_argument(arg, data_stack, x):
    if arg == 'X':
        return x
    if arg == 'X_NEGATIVE':
        return x * -1
    if arg == 'RESULT':
        return data_stack.pop()
    return arg


def calculate(tokens, min_x, max_x, precision=1.0) -> list:

    functions = deque()
    tokens_stack = deque()

    for token in tokens:
        if token.type is TokenType.NUMBER:
            tokens_stack.append(token.data)
        elif token.type is TokenType.X:
            tokens_stack.append('X')
        elif token.type is TokenType.X_NEGATIVE:
            tokens_stack.append('X_NEGATIVE')
        elif token.type in TokenGroup.arithmetic or token.type is TokenType.POWER:
            arg_1 = tokens_stack.pop() if len(tokens_stack) > 0 else None
            arg_2 = tokens_stack.pop() if len(tokens_stack) > 0 else None
            functions.append(Action(actions[token.type], 2, arg_1, arg_2))
            tokens_stack.append('RESULT')
        elif token.type in TokenGroup.trigonometry:
            arg_1 = tokens_stack.pop() if len(tokens_stack) > 0 else None
            functions.append(Action(actions[token.type], 1, arg_1, None))
            tokens_stack.append('RESULT')
        elif token.type is TokenType.LOG or TokenType.ROOT:
            arg_1 = tokens_stack.pop() if len(tokens_stack) > 0 else None
            functions.append(Action(actions[token.type], 2, arg_1, token.data))
            tokens_stack.append('RESULT')

    x_values = arange(min_x, max_x + precision, precision)
    data_stack = deque()
    results = deque()
    for x in x_values:
        for func in functions:

            arg_1 = check_function_argument(func.arg_1, data_stack, x)
            if func.num_of_args == 1:
                result = func.function(arg_1)
                data_stack.append(result)
                continue

            arg_2 = check_function_argument(func.arg_2, data_stack, x)
            result = func.function(arg_1, arg_2)
            data_stack.append(result)

        results.append(data_stack[0])
        data_stack.clear()

    results = [round(x, 4) for x in results]

    if [token for token in tokens if token.type in (TokenType.DIVISION, TokenType.TANGENT)]:
        discontinuity_points = check_continuity(results)
        for index in discontinuity_points:
            results[index] = nan

    return results


