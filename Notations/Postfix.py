
import math
from Tokens.TokenUtils import TokenUtils
from Tokens.Token import TokenValue
from collections import deque


class Postfix:

    def __init__(self):
        self.stack = deque()
        self.postfix_list = []


    def create_postfix(self, tokens):
        for token in tokens:
            if token.value in TokenUtils.operation or token.value in TokenUtils.trigonometry or\
                    token.value is TokenValue.LOG:
                self.process_operator(token)
            elif token.value in TokenUtils.bracket:
                if token.value is TokenValue.BRACKET_LEFT:
                    self.stack.append(token)
                else:
                    self.process_bracket_right()
            else:
                self.postfix_list.append(token)

        while len(self.stack) > 0:
            self.postfix_list.append(self.stack.pop())
        return self.postfix_list


    def process_operator(self, token):
        if len(self.stack) == 0:
            self.stack.append(token)
            return

        if token.value in (TokenValue.PLUS, TokenValue.MINUS):
            tokens_to_remove_from_stack = [TokenValue.LOG]
            TokenUtils.append_operation(tokens_to_remove_from_stack)
            TokenUtils.append_trigonometry(tokens_to_remove_from_stack)
            self.process_stack_operator(token, tokens_to_remove_from_stack)
        elif token.value in (TokenValue.MULTIPLICATION, TokenValue.DIVISION):
            tokens_to_remove_from_stack = [TokenValue.MULTIPLICATION, TokenValue.DIVISION, TokenValue.LOG]
            TokenUtils.append_trigonometry(tokens_to_remove_from_stack)
            self.process_stack_operator(token, tokens_to_remove_from_stack)
        else:
            tokens_to_remove_from_stack = [TokenValue.LOG]
            TokenUtils.append_trigonometry(tokens_to_remove_from_stack)
            self.process_stack_operator(token, tokens_to_remove_from_stack)


    def process_stack_operator(self, token, token_values):
        current_stack = None if len(self.stack) == 0 else self.stack.pop()
        while current_stack is not None and current_stack.value in token_values:
            self.postfix_list.append(current_stack)
            current_stack = None if len(self.stack) == 0 else self.stack.pop()
        if current_stack is not None:
            self.stack.append(current_stack)
        self.stack.append(token)


    def process_bracket_right(self):
        current_stack = self.stack.pop()
        while current_stack.value is not TokenValue.BRACKET_LEFT:
            self.postfix_list.append(current_stack)
            current_stack = self.stack.pop()


    def calculate(self, min_x, max_x):
        calculation_stack = []
        for x in range(min_x, max_x + 1):
            calculation_stack.append(deque())

        for token in self.postfix_list:
            if token.value is TokenValue.NUMBER:
                for calculation in calculation_stack:
                    calculation.append(token.number)
            elif token.value == TokenValue.X:
                number = min_x
                for values in calculation_stack:
                    values.append(number)
                    number += 1
            elif token.value is TokenValue.X_NEGATIVE:
                number = min_x * -1
                for calculation in calculation_stack:
                    calculation.append(number)
                    number -= 1
            elif token.value in TokenUtils.operation:
                for calculation in calculation_stack:
                    number_1 = calculation.pop()
                    number_2 = calculation.pop()
                    if token.value == TokenValue.PLUS:
                        calculation.append(number_1 + number_2)
                    elif token.value == TokenValue.MINUS:
                        calculation.append(number_2 - number_1)
                    elif token.value == TokenValue.MULTIPLICATION:
                        calculation.append(number_1 * number_2)
                    elif token.value == TokenValue.DIVISION:
                        calculation.append(number_1 / number_2)
            elif token.value in TokenUtils.trigonometry:
                for calculation in calculation_stack:
                    number = calculation.pop()
                    radian = math.radians(number)
                    if token.value == TokenValue.SINE:
                        calculation.append(math.sin(radian))
                    elif token.value == TokenValue.COSINE:
                        calculation.append(math.cos(radian))
                    elif token.value == TokenValue.TANGENT:
                        calculation.append(math.tan(radian))
                    elif token.value == TokenValue.COTANGENT:
                        calculation.append(math.cos(radian) / math.sin(radian))

        results = []
        for calculation in calculation_stack:
            results.append(round(calculation[0], 2))

        return results


