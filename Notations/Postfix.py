
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
        results = []
        for x in range(min_x, max_x + 1):
            results.append(deque())

        for token in self.postfix_list:
            if token.value is TokenValue.NUMBER:
                for result in results:
                    result.append(token.number)
            elif token.value == TokenValue.X:
                number = min_x
                for result in results:
                    result.append(number)
                    number += 1
            elif token.value is TokenValue.X_NEGATIVE:
                number = min_x * -1
                for result in results:
                    result.append(number)
                    number -= 1
            elif token.value in TokenUtils.operation:
                for result in results:
                    number_1 = result.pop()
                    number_2 = result.pop()
                    if token.value == TokenValue.PLUS:
                        result.append(number_1 + number_2)
                    elif token.value == TokenValue.MINUS:
                        result.append(number_2 - number_1)
                    elif token.value == TokenValue.MULTIPLICATION:
                        result.append(number_1 * number_2)
                    elif token.value == TokenValue.DIVISION:
                        result.append(number_1 / number_2)
            elif token.value in TokenUtils.trigonometry:
                for result in results:
                    number = result.pop()
                    radian = math.radians(number)
                    if token.value == TokenValue.SINE:
                        result.append(math.sin(radian))
                    elif token.value == TokenValue.COSINE:
                        result.append(math.cos(radian))
                    elif token.value == TokenValue.TANGENT:
                        result.append(math.tan(radian))
                    elif token.value == TokenValue.COTANGENT:
                        result.append(math.cos(radian) / math.sin(radian))

        for result in results:
            result[0] = round(result[0], 2)

        return results


