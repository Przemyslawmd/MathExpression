
from Token.Token import Token, TokenType
from Errors import ErrorType, ErrorMessage
from Token.Validator import validate
from Token.PostParser import post_parse


class Parser:

    def __init__(self, expression):
        self.chars = [char for char in expression]
        self.chars.reverse()
        self.initial_len = len(self.chars)
        self.tokens = []
        self.bracket_validator = 0
        self.bracket_angle_validator = 0

        self.one_char_tokens = {
            '+': TokenType.PLUS,
            '-': TokenType.MINUS,
            '*': TokenType.MULTIPLICATION,
            '/': TokenType.DIVISION,
            'x': TokenType.X,
            '^': TokenType.POWER
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


    def process_brackets(self, current_char, validator, left, right):
        if current_char == ')' or current_char == '>':
            if validator == 0:
                return 0
            self.tokens.append(Token(right))
            del self.chars[-1]
            return -1
        else:
            self.tokens.append(Token(left))
            del self.chars[-1]
            return 1


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
            if current_char == '(' or current_char == ')':
                result = self.process_brackets(current_char,
                                               self.bracket_validator,
                                               TokenType.BRACKET_LEFT,
                                               TokenType.BRACKET_RIGHT)
                if result == 0:
                    position = self.initial_len - len(self.chars) + 1
                    raise Exception(ErrorMessage[ErrorType.PARSER_BRACKET] + f": position {position}")
                self.bracket_validator += result
                continue
            if current_char == '<' or current_char == '>':
                result = self.process_brackets(current_char,
                                               self.bracket_angle_validator,
                                               TokenType.BRACKET_ANGLE_LEFT,
                                               TokenType.BRACKET_ANGLE_RIGHT)
                if result == 0:
                    position = self.initial_len - len(self.chars) + 1
                    raise Exception(ErrorMessage[ErrorType.PARSER_BRACKET_ANGLE] + f": position {position}")
                self.bracket_angle_validator += result
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

        if self.bracket_validator != 0:
            raise Exception(ErrorMessage[ErrorType.PARSER_BRACKET])
        if self.bracket_angle_validator != 0:
            raise Exception(ErrorMessage[ErrorType.PARSER_BRACKET_ANGLE])

        try:
            post_parse(self.tokens)
            validate(self.tokens)
        except Exception as e:
            raise Exception(e)

        return self.tokens


