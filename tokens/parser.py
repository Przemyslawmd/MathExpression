
from collections import deque

from errors import Error, ErrorMessage
from errorStorage import ErrorStorage
from tokens.postParser import add_multiplication_tokens, remove_angle_brackets, remove_negative_tokens
from tokens.token import Token, TokenType
from tokens.validator import validate_final, validate_brackets


one_char_tokens = {
    '+': TokenType.PLUS,
    '-': TokenType.MINUS,
    '*': TokenType.MULTIPLICATION,
    '/': TokenType.DIVISION,
    'x': TokenType.X,
    '^': TokenType.POWER,
    '(': TokenType.BRACKET_LEFT,
    ')': TokenType.BRACKET_RIGHT,
    '<': TokenType.BRACKET_ANGLE_LEFT,
    '>': TokenType.BRACKET_ANGLE_RIGHT
}


class Parser:

    def __init__(self, expression):
        self.char_stack = deque(char for char in reversed(expression))
        self.tokens_stack = deque()


    def pop_elements(self, number):
        for _ in range(number):
            self.char_stack.pop()


    def check_stack(self, *chars_to_check):
        shift = -1
        for char in chars_to_check:
            if self.char_stack[shift] != char:
                return False
            shift -= 1
        return True


    def add_number(self, char):
        number = int(char, 16)
        while bool(self.char_stack) and self.char_stack[-1].isdigit():
            number = number * 10 + int(self.char_stack.pop(), 16)
        self.tokens_stack.append(Token(TokenType.NUMBER, number))


    def check_multi_char_token(self, current_char):
        if len(self.char_stack) >= 1 and current_char == 't' and self.check_stack('g'):
            self.tokens_stack.append(Token(TokenType.TANGENT))
            self.char_stack.pop()
            return True
        if len(self.char_stack) >= 2:
            if current_char == 'c' and self.check_stack('o', 's'):
                self.tokens_stack.append(Token(TokenType.COSINE))
                self.pop_elements(2)
                return True
            if current_char == 'c' and self.check_stack('t', 'g'):
                self.tokens_stack.append(Token(TokenType.COTANGENT))
                self.pop_elements(2)
                return True
            if current_char == 's' and self.check_stack('i', 'n'):
                self.tokens_stack.append(Token(TokenType.SINE))
                self.pop_elements(2)
                return True
            if current_char == 'l' and self.check_stack('o', 'g'):
                self.tokens_stack.append(Token(TokenType.LOG, 10))
                self.pop_elements(2)
                return True
        if len(self.char_stack) >= 3 and current_char == 's' and self.check_stack('q', 'r', 't'):
            self.tokens_stack.append(Token(TokenType.ROOT, 2))
            self.pop_elements(3)
            return True
        else:
            return False


    def check_negative(self):
        if len(self.tokens_stack) == 0 or self.tokens_stack[-1].type in [TokenType.BRACKET_LEFT,
                                                                         TokenType.MULTIPLICATION,
                                                                         TokenType.DIVISION,
                                                                         TokenType.PLUS]:
            self.tokens_stack.append(Token(TokenType.NEGATIVE))
            return True
        if bool(self.char_stack) and self.char_stack[-1] not in [')', '*', '/']:
            self.tokens_stack.append(Token(TokenType.MINUS))
            return True
        return False


    def parse(self) -> list:
        while bool(self.char_stack):
            current_char = self.char_stack.pop()
            if current_char == ' ':
                continue
            elif current_char.isdigit():
                self.add_number(current_char)
            elif self.check_multi_char_token(current_char):
                continue
            else:
                token_symbol = one_char_tokens.get(current_char)
                if token_symbol is None:
                    ErrorStorage.putError(ErrorMessage[Error.PARSER_SYMBOL] + f": {current_char}")
                    return None
                if token_symbol is TokenType.MINUS:
                    if not self.check_negative():
                        ErrorStorage.putError(ErrorMessage[Error.PARSER_NEGATIVE_SYMBOL])
                        return None
                else:
                    self.tokens_stack.append(Token(token_symbol))

        tokens_list = list(self.tokens_stack)
        error = validate_brackets(tokens_list)
        if error != Error.NO_ERROR:
            ErrorStorage.putError(ErrorMessage[error])
            return None
        if not remove_angle_brackets(tokens_list):
            ErrorStorage.putError(ErrorMessage[Error.PARSER_BRACKET_ANGLE])
            return None
        add_multiplication_tokens(tokens_list)
        if not remove_negative_tokens(tokens_list):
            ErrorStorage.putError(ErrorMessage[Error.PARSER_NEGATIVE_SYMBOL])
            return None
        error = validate_final(tokens_list)
        if error != Error.NO_ERROR:
            ErrorStorage.putError(ErrorMessage[error])
            return None
        return tokens_list


