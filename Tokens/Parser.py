
from Tokens.Token import Token, TokenValue
from Tokens.TokenUtils import TokenUtils

class Parser:

    def __init__(self, expression):
        self.chars = [char for char in expression]
        self.initial_len = len(self.chars)
        self.chars.reverse()
        self.tokens = []
        self.bracket_validator = 0

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
                self.tokens.append(Token(TokenValue.LOG))
                del self.chars[-3:]
                return True
        if len(self.chars) >= 4 and self.chars[-4:] == self.root_chars:
            self.tokens.append(Token(TokenValue.ROOT))
            del self.chars[-4:]
            return True
        else:
            return False


    def check_brackets(self, current_char):
        if current_char == ')':
            self.bracket_validator -= 1
            if self.bracket_validator < 0:
                return False
            self.tokens.append(Token(TokenValue.BRACKET_RIGHT))
        else:
            self.bracket_validator += 1
            self.tokens.append(Token(TokenValue.BRACKET_LEFT))
        del self.chars[-1]
        return True


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
                    raise Exception(f"Parser error: improper symbol: {current_char}")
                continue
            if current_char == '(' or current_char == ')':
                if not self.check_brackets(current_char):
                    position = self.initial_len - len(self.chars) + 1
                    raise Exception(f"Error: improper bracket at position {position}")
                continue
            else:
                token_symbol = self.one_char_tokens.get(current_char)
                if token_symbol is None:
                    raise Exception(f"Parser error: improper symbol: {current_char}")
                elif token_symbol is TokenValue.MINUS:
                    if not self.check_negative():
                        position = self.initial_len - len(self.chars)
                        raise Exception(f"Parser error: improper usage of negative symbol at position: {position}")
                else:
                    self.tokens.append(Token(token_symbol))
                    del self.chars[-1]

        if self.bracket_validator != 0:
            raise Exception("Parser error: improper brackets")
        self.add_multiplication()
        if not self.remove_negative_tokens():
            raise Exception("Parser error: improper usage of negative symbol")

        return self.tokens


