import math

from Tokens.TokenUtils import TokenUtils
from Tokens.Token import TokenType, TokenValue
from collections import deque


class Postfix:

    def __init__(self):
        self.stack = deque()
        self.postfix_list = []


    def create_postfix(self, tokens):
        for token in tokens:
            if token.token_value in TokenUtils.operation or token.token_value in TokenUtils.trigonometry:
                self.process_operator(token)
            elif token.token_type is TokenType.BRACKET:
                if token.token_value is TokenValue.BRACKET_LEFT:
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

        if token.token_value in (TokenValue.PLUS, TokenValue.MINUS):
            self.process_stack_operator(token, [TokenValue.PLUS,
                                                TokenValue.MINUS,
                                                TokenValue.MULTIPLICATION,
                                                TokenValue.DIVISION,
                                                TokenValue.SINE,
                                                TokenValue.COSINE,
                                                TokenValue.TANGENT,
                                                TokenValue.COTANGENT])
        elif token.token_value in (TokenValue.MULTIPLICATION, TokenValue.DIVISION):
            self.process_stack_operator(token, [TokenValue.MULTIPLICATION,
                                                TokenValue.DIVISION,
                                                TokenValue.SINE,
                                                TokenValue.COSINE,
                                                TokenValue.TANGENT,
                                                TokenValue.COTANGENT])
        else:
            self.process_stack_operator(token, [TokenValue.SINE, TokenValue.COSINE, TokenValue.TANGENT, TokenValue.COTANGENT])


    def process_stack_operator(self, token, token_values):
        current_stack = None if len(self.stack) == 0 else self.stack.pop()
        while current_stack is not None and current_stack.token_value in token_values:
            self.postfix_list.append(current_stack)
            current_stack = None if len(self.stack) == 0 else self.stack.pop()
        if current_stack is not None:
            self.stack.append(current_stack)
        self.stack.append(token)


    def process_bracket_right(self):
        current_stack = self.stack.pop()
        while current_stack.token_value is not TokenValue.BRACKET_LEFT:
            self.postfix_list.append(current_stack)
            current_stack = self.stack.pop()


    def calculate(self, min_x, max_x):
        results = []
        for x in range(min_x, max_x + 1):
            results.append(deque())

        for token in self.postfix_list:
            if token.token_type == TokenType.NUMBER:
                for result in results:
                    result.append(token.token_number)
            elif token.token_value == TokenValue.X:
                number = min_x
                for result in results:
                    result.append(number)
                    number += 1
            elif token.token_value is TokenValue.X_NEGATIVE:
                number = min_x * -1
                for result in results:
                    result.append(number)
                    number -= 1
            elif token.token_type == TokenType.OPERATION:
                for result in results:
                    number_1 = result.pop()
                    number_2 = result.pop()
                    if token.token_value == TokenValue.PLUS:
                        result.append(number_1 + number_2)
                    elif token.token_value == TokenValue.MINUS:
                        result.append(number_2 - number_1)
                    elif token.token_value == TokenValue.MULTIPLICATION:
                        result.append(number_1 * number_2)
                    elif token.token_value == TokenValue.DIVISION:
                        result.append(number_1 / number_2)
            elif token.token_value in TokenUtils.trigonometry:
                for result in results:
                    number = result.pop()
                    radian = math.radians(number)
                    if token.token_value == TokenValue.SINE:
                        result.append(math.sin(radian))
                    elif token.token_value == TokenValue.COSINE:
                        result.append(math.cos(radian))
                    elif token.token_value == TokenValue.TANGENT:
                        result.append(math.tan(radian))
                    elif token.token_value == TokenValue.COTANGENT:
                        result.append(math.cos(radian) / math.sin(radian))

        for result in results:
            result[0] = round(result[0], 2)

        return results


