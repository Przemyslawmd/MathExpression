
from Tokens.Token import Token, TokenValue
from Tokens.TokenUtils import TokenUtils
from Errors import ErrorType, ErrorMessage
from Tokens.Validator import Validator

class Parser:

    def __init__(self, expression):
        self.chars = [char for char in expression]
        self.initial_len = len(self.chars)
        self.chars.reverse()
        self.tokens = []
        self.bracket_validator = 0
        self.bracket_square_validator = 0

        self.one_char_tokens = {
            '+': TokenValue.PLUS,
            '-': TokenValue.MINUS,
            '*': TokenValue.MULTIPLICATION,
            '/': TokenValue.DIVISION,
            'x': TokenValue.X,
            '^': TokenValue.POWER
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
        self.tokens.append(Token(TokenValue.NUMBER, number))


    def check_multiple_char_token(self):
        if len(self.chars) >= 2 and self.chars[-2:] == self.tangent_chars:
            self.tokens.append(Token(TokenValue.TANGENT))
            del self.chars[-2:]
            return True
        if len(self.chars) >= 3:
            if self.chars[-3:] == self.cosine_chars:
                self.tokens.append(Token(TokenValue.COSINE))
                del self.chars[-3:]
                return True
            if self.chars[-3:] == self.cotangent_chars:
                self.tokens.append(Token(TokenValue.COTANGENT))
                del self.chars[-3:]
                return True
            if self.chars[-3:] == self.sine_chars:
                self.tokens.append(Token(TokenValue.SINE))
                del self.chars[-3:]
                return True
            if self.chars[-3:] == self.log_chars:
                self.tokens.append(Token(TokenValue.LOG, 10))
                del self.chars[-3:]
                return True
        if len(self.chars) >= 4 and self.chars[-4:] == self.root_chars:
            self.tokens.append(Token(TokenValue.ROOT, 2))
            del self.chars[-4:]
            return True
        else:
            return False


    def process_brackets(self, current_char, validator, left, right):
        if current_char == ')' or current_char == ']':
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
        if len(self.chars) == self.initial_len - 1 or self.tokens[-1].value in [TokenValue.BRACKET_LEFT,
                                                                                TokenValue.MULTIPLICATION,
                                                                                TokenValue.DIVISION,
                                                                                TokenValue.PLUS]:
            self.tokens.append(Token(TokenValue.NEGATIVE))
        elif not self.chars or self.chars[-1] in [')', '*', '/']:
            return False
        else:
            self.tokens.append(Token(TokenValue.MINUS))
        return True


    def add_multiplication(self):
        indices = []
        for index, token in enumerate(self.tokens[:-1]):
            if token.value in [TokenValue.BRACKET_RIGHT, TokenValue.X, TokenValue.NUMBER]:
                next_token = self.tokens[index + 1]
                if next_token.value in [TokenValue.SINE,
                                        TokenValue.COSINE,
                                        TokenValue.TANGENT,
                                        TokenValue.COTANGENT,
                                        TokenValue.X,
                                        TokenValue.NUMBER,
                                        TokenValue.BRACKET_LEFT,
                                        TokenValue.ROOT]:
                    indices.append(index + 1)
        index_shift = 0
        for index in indices:
            self.tokens.insert(index + index_shift, Token(TokenValue.MULTIPLICATION))
            index_shift += 1


    def remove_negative_tokens(self):
        is_token_negative = False
        for index, token in enumerate(self.tokens):
            if token.value is TokenValue.NEGATIVE:
                is_token_negative = True
                continue
            if is_token_negative:
                if token.value is TokenValue.NUMBER:
                    number = token.data
                    self.tokens[index] = Token(TokenValue.NUMBER, number * -1)
                elif token.value is TokenValue.X:
                    self.tokens[index] = Token(TokenValue.X_NEGATIVE)
                elif token.value in [TokenValue.BRACKET_LEFT, TokenValue.ROOT, TokenValue.LOG, TokenUtils.trigonometry]:
                    self.tokens.insert(index, Token(TokenValue.MULTIPLICATION))
                    self.tokens.insert(index, Token(TokenValue.NUMBER, -1))
                else:
                    return False
                is_token_negative = False

        for i in range(len(self.tokens) - 1, -1, -1):
            if self.tokens[i].value is TokenValue.NEGATIVE:
                del self.tokens[i]
        return True


    def remove_square_brackets(self):
        tokens_to_remove = []
        for index, token in enumerate(self.tokens):
            if token.value is TokenValue.BRACKET_SQUARE_LEFT:
                if index == 0:
                    raise Exception(ErrorMessage[ErrorType.PARSER_BRACKET_SQUARE])
                if self.tokens[index - 1].value not in [TokenValue.ROOT, TokenValue.LOG]:
                    raise Exception(ErrorMessage[ErrorType.PARSER_BRACKET_SQUARE])
                if self.tokens[index + 1].value is not TokenValue.NUMBER:
                    raise Exception(ErrorMessage[ErrorType.PARSER_BRACKET_SQUARE])
                if self.tokens[index + 2].value is not TokenValue.BRACKET_SQUARE_RIGHT:
                    raise Exception(ErrorMessage[ErrorType.PARSER_BRACKET_SQUARE])
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
                                               TokenValue.BRACKET_LEFT,
                                               TokenValue.BRACKET_RIGHT)
                if result == 0:
                    position = self.initial_len - len(self.chars) + 1
                    raise Exception(ErrorMessage[ErrorType.PARSER_BRACKET] + f": position {position}")
                self.bracket_validator += result
                continue
            if current_char == '[' or current_char == ']':
                result = self.process_brackets(current_char,
                                               self.bracket_square_validator,
                                               TokenValue.BRACKET_SQUARE_LEFT,
                                               TokenValue.BRACKET_SQUARE_RIGHT)
                if result == 0:
                    position = self.initial_len - len(self.chars) + 1
                    raise Exception(ErrorMessage[ErrorType.PARSER_BRACKET_SQUARE] + f": position {position}")
                self.bracket_square_validator += result
                continue
            else:
                token_symbol = self.one_char_tokens.get(current_char)
                if token_symbol is None:
                    raise Exception(ErrorMessage[ErrorType.PARSER_SYMBOL] + f": {current_char}")
                elif token_symbol is TokenValue.MINUS:
                    if not self.check_negative():
                        position = self.initial_len - len(self.chars)
                        raise Exception(ErrorMessage[ErrorType.PARSER_NEGATIVE_SYMBOL] + f": position: {position}")
                else:
                    self.tokens.append(Token(token_symbol))
                    del self.chars[-1]

        if self.bracket_validator != 0:
            raise Exception(ErrorMessage[ErrorType.PARSER_BRACKET])
        if self.bracket_square_validator != 0:
            raise Exception(ErrorMessage[ErrorType.PARSER_BRACKET_SQUARE])
        self.remove_square_brackets()

        self.add_multiplication()
        if not self.remove_negative_tokens():
            raise Exception(ErrorMessage[ErrorType.PARSER_NEGATIVE_SYMBOL])

        validator = Validator()
        try:
            validator.validate(self.tokens)
        except Exception as e:
            raise Exception(e)

        return self.tokens


