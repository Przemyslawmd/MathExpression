
from collections import deque, namedtuple
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


Action = namedtuple('Action', ('function', 'arg_1', 'arg_2'))


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


def build_functions(tokens) -> list:
    functions = []
    args = deque()

    for token in tokens:
        if token.type is TokenType.NUMBER:
            args.append(token.data)
        elif token.type is TokenType.X:
            args.append('X')
        elif token.type in TokenGroup.arithmetic or token.type is TokenType.POWER:
            arg_1 = args.pop()
            arg_2 = args.pop()
            functions.append(Action(actions[token.type], arg_1, arg_2))
            args.append('RESULT')
        elif token.type in TokenGroup.trigonometry:
            arg_1 = args.pop()
            functions.append(Action(actions[token.type], arg_1, None))
            args.append('RESULT')
        elif token.type is TokenType.LOG or TokenType.ROOT:
            arg_1 = args.pop()
            functions.append(Action(actions[token.type], arg_1, token.data))
            args.append('RESULT')
    return functions


def calculate(tokens, min_x, max_x, precision=1.0) -> list:
    functions = build_functions(tokens)
    x_values = arange(min_x, max_x + precision, precision)
    data_stack = deque()
    results = deque()
    for x in x_values:
        for func in functions:
            arg_1 = data_stack.pop() if func.arg_1 == 'RESULT' else x if func.arg_1 == 'X' else func.arg_1
            if func.arg_2 is None:
                arg_1 = radians(arg_1)
                result = func.function(arg_1)
                data_stack.append(result)
                continue

            arg_2 = data_stack.pop() if func.arg_2 == 'RESULT' else x if func.arg_2 == 'X' else func.arg_2
            result = func.function(arg_1, arg_2)
            data_stack.append(result)

        results.append(data_stack[0])
        data_stack.clear()

    results = [round(x, 4) for x in results]

    division_or_tangent = filter(lambda t: t.type is TokenType.DIVISION or t.type is TokenType.TANGENT, tokens)
    if any(division_or_tangent):
        discontinuity_points = check_continuity(results)
        for index in discontinuity_points:
            results[index] = nan

    return results


def calculate_tree(root, min_x, max_x, precision = 1.0):
    add_leaves_data(root)
    x_values = arange(min_x, max_x + precision, precision)
    results = deque()
    for x in x_values:
        traverse(root, x)
        results.append(root.data)
    return results


def add_leaves_data(node):
    if node.left is not None:
        add_leaves_data(node.left)
    if node.right is not None:
        add_leaves_data(node.right)
    if node.token.type is TokenType.NUMBER:
        node.data = node.token.data


def traverse(node, x):
    if node.left is not None and node.left.token.type != TokenType.X and node.left.token.type != TokenType.NUMBER:
        traverse(node.left, x)
    if node.right is not None and node.right.token.type != TokenType.X and node.right.token.type != TokenType.NUMBER:
        traverse(node.right, x)
    operand_1 = x if node.left.token.type is TokenType.X else node.left.data
    operand_2 = x if node.right.token.type is TokenType.X else node.right.data
    func = actions[node.token.type]
    node.data = func(operand_2, operand_1)

