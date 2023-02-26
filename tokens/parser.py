
from Errors import ErrorType, ErrorMessage
from tokens.postParser import post_parse
from tokens.token import Token, TokenType
from tokens.validator import validate_final, validate_brackets


class Parser:

    def __init__(self, expression):
        self.chars = [char for char in expression]
        self.chars.reverse()
        self.initial_len = len(self.chars)
        self.tokens = []

        self.one_char_tokens = {
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

        self.cosine = ['s', 'o', 'c']
        self.cotangent = ['g', 't', 'c']
        self.logarithm = ['g', 'o', 'l']
        self.root = ['t', 'r', 'q', 's']
        self.sine = ['n', 'i', 's']
        self.tangent = ['g', 't']


    def add_number(self):
        number = int(self.chars.pop(), 16)
        while self.chars and self.chars[-1].isdigit():
            number = number * 10 + int(self.chars.pop(), 16)
        self.tokens.append(Token(TokenType.NUMBER, number))


    def check_multi_char_token(self):
        if len(self.chars) >= 2 and self.chars[-2:] == self.tangent:
            self.tokens.append(Token(TokenType.TANGENT))
            del self.chars[-2:]
            return True
        if len(self.chars) >= 3:
            if self.chars[-3:] == self.cosine:
                self.tokens.append(Token(TokenType.COSINE))
                del self.chars[-3:]
                return True
            if self.chars[-3:] == self.cotangent:
                self.tokens.append(Token(TokenType.COTANGENT))
                del self.chars[-3:]
                return True
            if self.chars[-3:] == self.sine:
                self.tokens.append(Token(TokenType.SINE))
                del self.chars[-3:]
                return True
            if self.chars[-3:] == self.logarithm:
                self.tokens.append(Token(TokenType.LOG, 10))
                del self.chars[-3:]
                return True
        if len(self.chars) >= 4 and self.chars[-4:] == self.root:
            self.tokens.append(Token(TokenType.ROOT, 2))
            del self.chars[-4:]
            return True
        else:
            return False


    def check_negative(self):
        del self.chars[-1]
        if len(self.tokens) == 0 or self.tokens[-1].type in [TokenType.BRACKET_LEFT,
                                                             TokenType.MULTIPLICATION,
                                                             TokenType.DIVISION,
                                                             TokenType.PLUS]:
            self.tokens.append(Token(TokenType.NEGATIVE))
        elif not self.chars or self.chars[-1] in [')', '*', '/']:
            return False
        else:
            self.tokens.append(Token(TokenType.MINUS))
        return True


    def parse(self):
        while self.chars:
            current_char = self.chars[-1]
            if current_char == ' ':
                del self.chars[-1]
                continue
            if current_char.isdigit():
                self.add_number()
                continue
            if self.check_multi_char_token():
                continue
            else:
                token_symbol = self.one_char_tokens.get(current_char)
                if token_symbol is None:
                    raise Exception(ErrorMessage[ErrorType.PARSER_SYMBOL] + f": {current_char}")
                elif token_symbol is TokenType.MINUS:
                    if not self.check_negative():
                        position = self.initial_len - len(self.chars)
                        raise Exception(ErrorMessage[ErrorType.PARSER_NEGATIVE_SYMBOL] + f": position: {position}")
                else:
                    self.tokens.append(Token(token_symbol))
                    del self.chars[-1]

        try:
            validate_brackets(self.tokens)
            post_parse(self.tokens)
            validate_final(self.tokens)
        except Exception as e:
            raise Exception(e)

        return self.tokens


