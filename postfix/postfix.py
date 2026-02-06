
from collections import deque

from tokens.token import TokenType
from tokens.tokenGroup import TokenGroup


class Postfix:

    def __init__(self):
        self.stack = deque()
        self.postfix = deque()
        self.operator_not_plus_minus = [t for t in TokenGroup.operators if t not in (TokenType.PLUS, TokenType.MINUS)]
        self.operator_not_arithmetic = [t for t in TokenGroup.operators if t not in TokenGroup.arithmetic]


    def create_postfix(self, tokens) -> deque:
        for token in tokens:
            if token.type in TokenGroup.operators:
                self.check_operator(token)
            elif token.type is TokenType.BRACKET_LEFT:
                self.stack.append(token)
            elif token.type is TokenType.BRACKET_RIGHT:
                self.process_bracket_right()
            else:
                self.postfix.append(token)

        while self.stack:
            self.postfix.append(self.stack.pop())
        return self.postfix

    # ------------------------------- INTERNAL ----------------------------------- #

    def check_operator(self, token) -> None:
        if not self.stack:
            self.stack.append(token)
            return

        if token.type in (TokenType.PLUS, TokenType.MINUS):
            self.move_tokens(TokenGroup.operators)
        elif token.type in (TokenType.MULTIPLICATION, TokenType.DIVISION):
            self.move_tokens(self.operator_not_plus_minus)
        elif token.type in (TokenGroup.trigonometry, TokenType.LOG, TokenType.ROOT):
            self.move_tokens(self.operator_not_arithmetic)
        else:
            self.move_tokens([TokenType.POWER])
        self.stack.append(token)


    def move_tokens(self, tokens_to_move) -> None:
        stack_token = None if not self.stack else self.stack.pop()
        while stack_token and stack_token.type in tokens_to_move:
            self.postfix.append(stack_token)
            stack_token = None if not self.stack else self.stack.pop()
        if stack_token:
            self.stack.append(stack_token)


    def process_bracket_right(self) -> None:
        current_stack = self.stack.pop()
        while current_stack.type is not TokenType.BRACKET_LEFT:
            self.postfix.append(current_stack)
            current_stack = self.stack.pop()

