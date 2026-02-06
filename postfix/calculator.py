
from collections import deque
from enum import Enum

from math import cos, log, nan, radians, sin, sqrt, tan
from numpy import power

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
    TokenType.POWER: lambda a, b: nan if ((float(a).is_integer() is False and b < 0) or (b == 0 and a < 0))
                                      else power(b, a),
    TokenType.ROOT: lambda a, b: nan if a < 0 else (sqrt(a) if b == 2 else power(a, 1 / b)),

    TokenType.COSINE: lambda a: cos(a),
    TokenType.COTANGENT: lambda a: nan if round(sin(a), 4) == 0.00 else cos(a) / sin(a),
    TokenType.SINE: lambda a: sin(a),
    TokenType.TANGENT: lambda a: nan if round(cos(a), 4) == 0.00 else tan(a),
}

def calculate(root, x_values, continuity = False) -> list:
    add_leaves_data(root)
    results = deque()
    for x in x_values:
        traverse(root, x)
        results.append(root.data)
    results = [round(x, 4) for x in results]

    if continuity:
        discontinuity_points = check_continuity(results)
        for index in discontinuity_points:
            results[index] = nan
    return results

# ------------------------------- INTERNAL ----------------------------------- #

def check_directions(numbers) -> list:
    directions = [Direction.NONE] * len(numbers)
    for i, number in enumerate(numbers):
        if i == 0:
            continue
        if number > numbers[i - 1]:
            directions[i] = Direction.UP
        elif number < numbers[i - 1]:
            directions[i] = Direction.DOWN
        else:
            directions[i] = Direction.CONST
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
    for i, direction in enumerate(directions):
        if direction != directions[i - 1]:
            if is_discontinuity(directions[i - 1], direction, numbers[i - 1], numbers[i]):
                discontinuity_points.append(i)
    return discontinuity_points


def add_leaves_data(node) -> None:
    if node.left is not None:
        add_leaves_data(node.left)
    if node.right:
        add_leaves_data(node.right)
    if node.token.type is TokenType.NUMBER:
        node.data = node.token.data


def traverse(node, x) -> None:
    left = node.left
    right = node.right
    if left and left.token.type not in TokenGroup.operand:
        traverse(left, x)
    if right and right.token.type not in TokenGroup.operand:
        traverse(right, x)
    if node.token.type in TokenGroup.trigonometry:
        operand = radians(x) if left.token.type is TokenType.X else radians(left.data)
        node.data = actions[node.token.type](operand)
    elif node.token.type is TokenType.ROOT or node.token.type is TokenType.LOG:
        operand_1 = x if left.token.type is TokenType.X else left.data
        operand_2 = node.token.data
        node.data = actions[node.token.type](operand_1, operand_2)
    else:
        operand_1 = x if left.token.type is TokenType.X else left.data
        operand_2 = x if right.token.type is TokenType.X else right.data
        node.data = actions[node.token.type](operand_2, operand_1)

