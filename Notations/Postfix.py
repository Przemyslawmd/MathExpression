
from Tokens.Token import TokenType
from Tokens.Token import TokenValue


class Postfix:

    def __init__(self):
        self.stack = []
        self.postfix_list = []

    def create_postfix(self, token_group_list):
        for token_group in token_group_list:
            if token_group[0].token_type is TokenType.OPERATION:
                self.process_operator(token_group[0])
            elif token_group[0].token_type is TokenType.BRACKET:
                if token_group[0].token_value is TokenValue.BRACKET_LEFT:
                    self.stack.append(token_group[0])
                else:
                    self.process_bracket_right(self, token_group)
            else:
                self.postfix_list.append(token_group)

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
        current_stack_index = len(self.stack) - 1
        self.stack.pop(current_stack_index)
        current_stack_index -= 1
        while True:
            if current_stack_index < 0:
                raise Exception("No correspoding left bracket")
            if self.stack[current_stack_index].token_value is TokenValue.BRACKET_LEFT:
                self.stack.pop(current_stack_index)
                return
            else:
                self.postfix_list.append(self.stack[current_stack_index])
                self.stack.pop(current_stack_index)
                current_stack_index -= 1

