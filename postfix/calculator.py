import math
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


ABS_TOL_VAL = 0.00001

actions = {
    TokenType.DIVISION: lambda a, b: nan if math.isclose(a, 0, abs_tol = ABS_TOL_VAL) else b / a,
    TokenType.MINUS: lambda a, b: b - a,
    TokenType.MULTIPLICATION: lambda a, b: a * b,
    TokenType.PLUS: lambda a, b: a + b,

    TokenType.LOG: lambda a, b: log(a, b) if a > 0 else nan,
    TokenType.POWER: lambda a, b: nan if ((float(a).is_integer() is False and b < 0) or (b == 0 and a < 0))
                                      else power(b, a),
    TokenType.ROOT: lambda a, b: nan if a < 0 else (sqrt(a) if b == 2 else power(a, 1 / b)),

    TokenType.COSINE: lambda a: cos(a),
    TokenType.COTANGENT: lambda a: nan if math.isclose(sin(a), 0, abs_tol = ABS_TOL_VAL) else cos(a) / sin(a),
    TokenType.SINE: lambda a: sin(a),
    TokenType.TANGENT: lambda a: nan if math.isclose(cos(a), 0, abs_tol = ABS_TOL_VAL) else tan(a),
}


def calculate(root, x_values) -> list:
    add_leaves_data(root)
    results = deque()
    for x in x_values:
        traverse(root, x)
        results.append(root.data)
    return [x for x in results]

# ------------------------------- INTERNAL ----------------------------------- #

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

