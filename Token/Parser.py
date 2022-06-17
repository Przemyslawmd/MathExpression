
from Token.Token import Token, TokenType
from Token.TokenUtils import TokenUtils
from Errors import ErrorType, ErrorMessage
from Token.Validator import Validator


class Parser:

    def __init__(self, expression):
        self.chars = [char for char in expression]
        self.initial_len = len(self.chars)
        self.chars.reverse()
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

        # to recognize the beginning of multi chars tokens
        self.beginning_chars = ['c', 's', 'l', 't']

        self.cosine_chars = ['s', 'o', 'c']
        self.cotangent_chars = ['g', 't', 'c']
        self.log_chars = ['g', 'o', 'l']
        self.root_chars = ['t', 'r', 'q', 's']
        self.sine_chars = ['n', 'i', 's']
        self.tangent_chars = ['g', 't']


    def add_number(self):
        number = int(self.chars.pop(), 16)
        while self.chars and self.chars[-1].isdigit():
            number = number * 10 + int(self.chars.pop(), 16)
        self.tokens.append(Token(TokenType.NUMBER, number))


    def check_multiple_char_token(self):
        if len(self.chars) >= 2 and self.chars[-2:] == self.tangent_chars:
            self.tokens.append(Token(TokenType.TANGENT))
            del self.chars[-2:]
            return True
        if len(self.chars) >= 3:
            if self.chars[-3:] == self.cosine_chars:
                self.tokens.append(Token(TokenType.COSINE))
                del self.chars[-3:]
                return True
            if self.chars[-3:] == self.cotangent_chars:
                self.tokens.append(Token(TokenType.COTANGENT))
                del self.chars[-3:]
                return True
            if self.chars[-3:] == self.sine_chars:
                self.tokens.append(Token(TokenType.SINE))
                del self.chars[-3:]
                return True
            if self.chars[-3:] == self.log_chars:
                self.tokens.append(Token(TokenType.LOG, 10))
                del self.chars[-3:]
                return True
        if len(self.chars) >= 4 and self.chars[-4:] == self.root_chars:
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
        if len(self.chars) == self.initial_len - 1 or self.tokens[-1].type in [TokenType.BRACKET_LEFT,
                                                                               TokenType.MULTIPLICATION,
                                                                               TokenType.DIVISION,
                                                                               TokenType.PLUS]:
            self.tokens.append(Token(TokenType.NEGATIVE))
        elif not self.chars or self.chars[-1] in [')', '*', '/']:
            return False
        else:
            self.tokens.append(Token(TokenType.MINUS))
        return True


    def add_multiplication(self):
        indices = []
        for index, token in enumerate(self.tokens[:-1]):
            if token.type in [TokenType.BRACKET_RIGHT, TokenType.X, TokenType.NUMBER]:
                next_token = self.tokens[index + 1]
                if next_token.type in [TokenType.SINE,
                                       TokenType.COSINE,
                                       TokenType.TANGENT,
                                       TokenType.COTANGENT,
                                       TokenType.X,
                                       TokenType.NUMBER,
                                       TokenType.BRACKET_LEFT,
                                       TokenType.ROOT,
                                       TokenType.LOG]:
                    if token.type is TokenType.NUMBER and next_token.type is TokenType.NUMBER:
                        continue
                    indices.append(index + 1)
        index_shift = 0
        for index in indices:
            self.tokens.insert(index + index_shift, Token(TokenType.MULTIPLICATION))
            index_shift += 1


    def remove_negative_tokens(self):
        is_token_negative = False
        for index, token in enumerate(self.tokens):
            if token.type is TokenType.NEGATIVE:
                is_token_negative = True
                continue
            if is_token_negative:
                if token.type is TokenType.NUMBER:
                    number = token.data
                    self.tokens[index] = Token(TokenType.NUMBER, number * -1)
                elif token.type is TokenType.X:
                    self.tokens[index] = Token(TokenType.X_NEGATIVE)
                elif token.type in [TokenType.BRACKET_LEFT, TokenType.ROOT, TokenType.LOG, TokenUtils.trigonometry]:
                    self.tokens.insert(index, Token(TokenType.MULTIPLICATION))
                    self.tokens.insert(index, Token(TokenType.NUMBER, -1))
                else:
                    return False
                is_token_negative = False

        for i in range(len(self.tokens) - 1, -1, -1):
            if self.tokens[i].type is TokenType.NEGATIVE:
                del self.tokens[i]
        return True


    def remove_angle_brackets(self):
        tokens_to_remove = []
        for index, token in enumerate(self.tokens):
            if token.type is not TokenType.BRACKET_ANGLE_LEFT:
                continue
            if index == 0:
                raise Exception(ErrorMessage[ErrorType.PARSER_BRACKET_ANGLE])
            if self.tokens[index - 1].type not in [TokenType.ROOT, TokenType.LOG]:
                raise Exception(ErrorMessage[ErrorType.PARSER_BRACKET_ANGLE])
            if self.tokens[index + 1].type is not TokenType.NUMBER:
                raise Exception(ErrorMessage[ErrorType.PARSER_BRACKET_ANGLE])
            if self.tokens[index + 2].type is not TokenType.BRACKET_ANGLE_RIGHT:
                raise Exception(ErrorMessage[ErrorType.PARSER_BRACKET_ANGLE])
            self.tokens[index - 1].data = self.tokens[index + 1].data
            tokens_to_remove.append(index)
            tokens_to_remove.append(index + 1)
            tokens_to_remove.append(index + 2)

        for i in range(len(self.tokens) - 1, -1, -1):
            if i in tokens_to_remove:
                del self.tokens[i]


    def parse(self):
        while self.chars:
            current_char = self.chars[-1]
            if current_char == ' ':
                del self.chars[-1]
                continue
            if current_char.isdigit():
                self.add_number()
                continue
            if current_char in self.beginning_chars:
                if not self.check_multiple_char_token():
                    raise Exception(ErrorMessage[ErrorType.PARSER_SYMBOL] + f": {current_char}")
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
        self.remove_angle_brackets()

        self.add_multiplication()
        if not self.remove_negative_tokens():
            raise Exception(ErrorMessage[ErrorType.PARSER_NEGATIVE_SYMBOL])
        try:
            Validator().validate(self.tokens)
        except Exception as e:
            raise Exception(e)

        return self.tokens


