
import math
from numpy import power, arange

from Tokens.TokenUtils import TokenUtils
from Tokens.Token import TokenType
from collections import deque


class Calculator:

    def __init__(self):

        self.actions = {
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

    def calculate(self, postfix, min_x, max_x, x_precision=1.0):
        calculation_stack = deque()
        for _ in arange(min_x, max_x + x_precision, x_precision):
            calculation_stack.append(deque())

        for token in postfix:
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
            elif token.type in TokenUtils.basic_arithmetic or token.type is TokenType.POWER:
                for calculation in calculation_stack:
                    num_1 = calculation.pop()
                    num_2 = calculation.pop()
                    calculation.append(self.actions[token.type](num_1, num_2))
            elif token.type in TokenUtils.trigonometry:
                for calculation in calculation_stack:
                    num = calculation.pop()
                    radian = math.radians(num)
                    calculation.append(self.actions[token.type](radian))
            elif token.type is TokenType.LOG or TokenType.ROOT:
                for calculation in calculation_stack:
                    num = calculation.pop()
                    calculation.append(self.actions[token.type](num, token.data))

        return [round(x[0], 4) for x in calculation_stack]


