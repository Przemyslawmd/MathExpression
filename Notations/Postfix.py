
import math
from numpy import power, arange

from Tokens.TokenUtils import TokenUtils
from Tokens.Token import TokenType
from collections import deque


class Postfix:

    def __init__(self):
        self.stack = deque()
        self.postfix = deque()

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

    def create_postfix(self, tokens):
        for token in tokens:
            if token.type in TokenUtils.operators:
                self.process_operator(token)
            elif token.type is TokenType.BRACKET_LEFT:
                self.stack.append(token)
            elif token.type is TokenType.BRACKET_RIGHT:
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

        if token.type in (TokenType.PLUS, TokenType.MINUS):
            self.process_stack_operator(token, TokenUtils.operators)
        elif token.type in (TokenType.MULTIPLICATION, TokenType.DIVISION):
            tokens_to_move = [token for token in TokenUtils.operators if (token not in [TokenType.PLUS, TokenType.MINUS])]
            self.process_stack_operator(token, tokens_to_move)
        elif token.type in TokenUtils.trigonometry or token.type is TokenType.LOG or token.type is TokenType.ROOT:
            tokens_to_move = [token for token in TokenUtils.operators if (token not in TokenUtils.basic_arithmetic)]
            self.process_stack_operator(token, tokens_to_move)
        else:
            self.process_stack_operator(token, [TokenType.POWER])


    def process_stack_operator(self, token, token_values):
        current_stack = None if len(self.stack) == 0 else self.stack.pop()
        while current_stack is not None and current_stack.type in token_values:
            self.postfix.append(current_stack)
            current_stack = None if len(self.stack) == 0 else self.stack.pop()
        if current_stack is not None:
            self.stack.append(current_stack)
        self.stack.append(token)


    def process_bracket_right(self):
        current_stack = self.stack.pop()
        while current_stack.type is not TokenType.BRACKET_LEFT:
            self.postfix.append(current_stack)
            current_stack = self.stack.pop()


    def calculate(self, min_x, max_x, x_precision=1.0):
        calculation_stack = deque()
        for _ in arange(min_x, max_x + x_precision, x_precision):
            calculation_stack.append(deque())

        for token in self.postfix:
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


