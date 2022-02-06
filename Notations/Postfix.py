
import math

import numpy

from Tokens.TokenUtils import TokenUtils
from Tokens.Token import TokenValue
from collections import deque


class Postfix:

    def __init__(self):
        self.stack = deque()
        self.postfix = deque()

        self.actions = {
            TokenValue.DIVISION: lambda a, b: math.nan if round(a, 2) == 0.00 else b / a,
            TokenValue.MINUS: lambda a, b: b - a,
            TokenValue.MULTIPLICATION: lambda a, b: a * b,
            TokenValue.PLUS: lambda a, b: a + b,

            TokenValue.POWER: lambda a, b: math.pow(b, a),

            TokenValue.COSINE: lambda a: math.cos(a),
            TokenValue.COTANGENT: lambda a: math.nan if round(math.sin(a), 2) == 0.00 else math.cos(a) / math.sin(a),
            TokenValue.SINE: lambda a: math.sin(a),
            TokenValue.TANGENT: lambda a: math.tan(a),
        }

    def create_postfix(self, tokens):
        for token in tokens:
            if token.value in TokenUtils.operators:
                self.process_operator(token)
            elif token.value is TokenValue.BRACKET_LEFT:
                self.stack.append(token)
            elif token.value is TokenValue.BRACKET_RIGHT:
                self.process_bracket_right()
            else:
                self.postfix.append(token)

        while len(self.stack) > 0:
            self.postfix.append(self.stack.pop())
        return self.postfix


    def process_operator(self, token):
        if len(self.stack) == 0:
            self.stack.append(token)
            return

        if token.value in (TokenValue.PLUS, TokenValue.MINUS):
            self.process_stack_operator(token, TokenUtils.operators)
        elif token.value in (TokenValue.MULTIPLICATION, TokenValue.DIVISION):
            tokens_to_move = [token for token in TokenUtils.operators if (token not in [TokenValue.PLUS, TokenValue.MINUS])]
            self.process_stack_operator(token, tokens_to_move)
        elif token.value in TokenUtils.trigonometry or token.value is TokenValue.LOG:
            tokens_to_move = [token for token in TokenUtils.operators if (token not in TokenUtils.operation)]
            self.process_stack_operator(token, tokens_to_move)
        else:
            self.process_stack_operator(token, [TokenValue.POWER])


    def process_stack_operator(self, token, token_values):
        current_stack = None if len(self.stack) == 0 else self.stack.pop()
        while current_stack is not None and current_stack.value in token_values:
            self.postfix.append(current_stack)
            current_stack = None if len(self.stack) == 0 else self.stack.pop()
        if current_stack is not None:
            self.stack.append(current_stack)
        self.stack.append(token)


    def process_bracket_right(self):
        current_stack = self.stack.pop()
        while current_stack.value is not TokenValue.BRACKET_LEFT:
            self.postfix.append(current_stack)
            current_stack = self.stack.pop()


    def calculate(self, min_x, max_x, x_precision=1.0):
        calculation_stack = deque()
        for _ in numpy.arange(min_x, max_x + x_precision, x_precision):
            calculation_stack.append(deque())

        for token in self.postfix:
            if token.value is TokenValue.NUMBER:
                for calculation in calculation_stack:
                    calculation.append(token.number)
            elif token.value == TokenValue.X:
                number = min_x
                for values in calculation_stack:
                    values.append(number)
                    number += x_precision
            elif token.value is TokenValue.X_NEGATIVE:
                number = min_x * -1
                for calculation in calculation_stack:
                    calculation.append(number)
                    number -= x_precision
            elif token.value in TokenUtils.operation or token.value is TokenValue.POWER:
                for calculation in calculation_stack:
                    num_1 = calculation.pop()
                    num_2 = calculation.pop()
                    calculation.append(self.actions[token.value](num_1, num_2))
            elif token.value in TokenUtils.trigonometry:
                for calculation in calculation_stack:
                    num = calculation.pop()
                    radian = math.radians(num)
                    calculation.append(self.actions[token.value](radian))
            elif token.value is TokenValue.LOG:
                for calculation in calculation_stack:
                    number = calculation.pop()
                    result = math.log(number, 10) if number > 0 else math.nan
                    calculation.append(result)

        results = []
        for calculation in calculation_stack:
            results.append(round(calculation[0], 2))
        return results


