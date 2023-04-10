
from errors import Error, ErrorMessage
from tokens.postParser import post_parse
from tokens.token import Token, TokenType
from tokens.validator import validate_final, validate_brackets
from collections import deque

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
        self.initial_len = len(self.char_stack)
        self.tokens = []


    def pop_elements(self, number):
        for _ in range(number):
            self.char_stack.pop()


    def check_stack(self, *chars):
        shift = -1
        for char in chars:
            if self.char_stack[shift] != char:
                return False
            shift -= 1
        return True


    def add_number(self, char):
        number = int(char, 16)
        while bool(self.char_stack) and self.char_stack[-1].isdigit():
            number = number * 10 + int(self.char_stack.pop(), 16)
        self.tokens.append(Token(TokenType.NUMBER, number))


    def check_multi_char_token(self, current_char):
        if len(self.char_stack) >= 1 and self.check_stack('g'):
            self.tokens.append(Token(TokenType.TANGENT))
            self.char_stack.pop()
            return True
        if len(self.char_stack) >= 2:
            if current_char == 'c' and self.check_stack('o', 's'):
                self.tokens.append(Token(TokenType.COSINE))
                self.pop_elements(2)
                return True
            if current_char == 'c' and self.check_stack('t', 'g'):
                self.tokens.append(Token(TokenType.COTANGENT))
                self.pop_elements(2)
                return True
            if current_char == 's' and self.check_stack('i', 'n'):
                self.tokens.append(Token(TokenType.SINE))
                self.pop_elements(2)
                return True
            if current_char == 'l' and self.check_stack('o', 'g'):
                self.tokens.append(Token(TokenType.LOG, 10))
                self.pop_elements(2)
                return True
        if len(self.char_stack) >= 3 and current_char == 's' and self.check_stack('q', 'r', 't'):
            self.tokens.append(Token(TokenType.ROOT, 2))
            self.pop_elements(3)
            return True
        else:
            return False


    def check_negative(self):
        if len(self.tokens) == 0 or self.tokens[-1].type in [TokenType.BRACKET_LEFT,
                                                             TokenType.MULTIPLICATION,
                                                             TokenType.DIVISION,
                                                             TokenType.PLUS]:
            self.tokens.append(Token(TokenType.NEGATIVE))
            return True
        elif bool(self.char_stack) and self.char_stack[-1] not in [')', '*', '/']:
            self.tokens.append(Token(TokenType.MINUS))
            return True
        return False


    def parse(self):
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
                    raise Exception(ErrorMessage[Error.PARSER_SYMBOL] + f": {current_char}")
                elif token_symbol is TokenType.MINUS:
                    if not self.check_negative():
                        position = self.initial_len - len(self.char_stack)
                        raise Exception(ErrorMessage[Error.PARSER_NEGATIVE_SYMBOL] + f": position: {position}")
                else:
                    self.tokens.append(Token(token_symbol))
        try:
            validate_brackets(self.tokens)
            post_parse(self.tokens)
            validate_final(self.tokens)
        except Exception as e:
            raise Exception(e)

        return self.tokens


