
from collections import deque

from tokens.token import TokenType
from tokens.tokenGroup import TokenGroup


class Postfix:

    def __init__(self):
        self.stack = deque()
        self.postfix = deque()

    def create_postfix(self, tokens):
        for token in tokens:
            if token.type in TokenGroup.operators:
                self.process_operator(token)
            elif token.type is TokenType.BRACKET_LEFT:
                self.stack.append(token)
            elif token.type is TokenType.BRACKET_RIGHT:
                self.process_bracket_right()
            else:
                self.postfix.append(token)

        while self.stack:
            self.postfix.append(self.stack.pop())
        return self.postfix


    def process_operator(self, token):
        if not self.stack:
            self.stack.append(token)
            return

        if token.type in (TokenType.PLUS, TokenType.MINUS):
            self.process_stack_operator(token, TokenGroup.operators)
        elif token.type in (TokenType.MULTIPLICATION, TokenType.DIVISION):
            tokens_to_move = [token for token in TokenGroup.operators if (token not in [TokenType.PLUS, TokenType.MINUS])]
            self.process_stack_operator(token, tokens_to_move)
        elif token.type in TokenGroup.trigonometry or token.type is TokenType.LOG or token.type is TokenType.ROOT:
            tokens_to_move = [token for token in TokenGroup.operators if (token not in TokenGroup.basic_arithmetic)]
            self.process_stack_operator(token, tokens_to_move)
        else:
            self.process_stack_operator(token, [TokenType.POWER])


    def process_stack_operator(self, token, token_values):
        current_stack = None if not self.stack else self.stack.pop()
        while current_stack and current_stack.type in token_values:
            self.postfix.append(current_stack)
            current_stack = None if not self.stack else self.stack.pop()
        if current_stack:
            self.stack.append(current_stack)
        self.stack.append(token)


    def process_bracket_right(self):
        current_stack = self.stack.pop()
        while current_stack.type is not TokenType.BRACKET_LEFT:
            self.postfix.append(current_stack)
            current_stack = self.stack.pop()


