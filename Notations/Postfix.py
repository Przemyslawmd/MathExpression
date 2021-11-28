
from Tokens.Token import TokenType, TokenValue
from collections import deque


class Postfix:

    def __init__(self):
        self.stack = deque()
        self.postfix_list = []


    def create_postfix(self, tokens):
        for token in tokens:
            if token.token_type is TokenType.OPERATION:
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
            self.process_stack_operator(token, [TokenValue.PLUS, TokenValue.MINUS, TokenValue.MULTIPLICATION, TokenValue.DIVISION])
        else:
            self.process_stack_operator(token, [TokenValue.MULTIPLICATION, TokenValue.DIVISION])


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


    def calculate(self, min, max):
        results = []
        for x in range(min, max + 1):
            results.append(deque())

        for token in self.postfix_list:
            if token.token_type == TokenType.NUMBER:
                for result in results:
                    result.append(token.token_number)
            elif token.token_value == TokenValue.X:
                number = min
                for result in results:
                    result.append(number)
                    number += 1
            elif token.token_type == TokenType.OPERATION:
                for result in results:
                    number_1 = result.pop()
                    number_2 = result.pop()
                    if token.token_value == TokenValue.PLUS:
                        result.append(number_1 + number_2)
                    elif token.token_value == TokenValue.MINUS:
                        result.append(number_1 - number_2)
                    elif token.token_value == TokenValue.MULTIPLICATION:
                        result.append(number_1 * number_2)
                    elif token.token_value == TokenValue.DIVISION:
                        result.append(number_1 / number_2)
        return results
