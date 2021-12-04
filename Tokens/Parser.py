
from Tokens.Token import Token, TokenValue


class Parser:

    def __init__(self, expression):

        self.expression = expression.replace(" ",'')
        self.tokens = []
        self.bracket_validator = 0
        self.index = 0

        self.other_symbols_map = {
            '+': TokenValue.PLUS,
            '-': TokenValue.MINUS,
            '*': TokenValue.MULTIPLICATION,
            '/': TokenValue.DIVISION,
            'x': TokenValue.X
        }

    def add_number(self, index):
        number = int(self.expression[index], 16)
        shift = 1
        while (index + shift) < len(self.expression) and self.expression[index + shift].isdigit():
            number = number * 10 + int(self.expression[index + shift])
            shift += 1
        self.tokens.append(Token(TokenValue.NONE, number))
        self.index += shift


    def check_ctg_or_cos(self, index):
        if self.expression[index + 1] == 'o' and self.expression[index + 2] == 's':
            self.tokens.append(Token(TokenValue.COSINE, 0))
        elif self.expression[index + 1] == 't' and self.expression[index + 2] == 'g':
            self.tokens.append(Token(TokenValue.COTANGENT, 0))
        else:
            raise Exception("Parse failed: improper symbol at index " + str(index + 1) + " or " + str(index + 2))
        self.index += 3


    def check_sine(self, index):
        if self.expression[index + 1] == 'i' and self.expression[index + 2] == 'n':
            self.tokens.append(Token(TokenValue.SINE, 0))
        else:
            raise Exception("Parse failed: improper symbol at index: " + str(index + 1) + " or " + str(index + 2))
        self.index += 3

    def check_tg(self, index):
        if self.expression[index + 1] == 'g':
            self.tokens.append(Token(TokenValue.TANGENT, 0))
        else:
            raise Exception("Parse failed: improper symbol at index " + str(index + 1))
        self.index += 2

    def check_log(self, index):
        if self.expression[index + 1] == 'o' and self.expression[index + 2] == 'g':
            self.tokens.append(Token(TokenValue.LOG, 0))
        else:
            raise Exception("Parse failed: improper symbol at index " + str(index + 1) + " or " + str(index + 2))
        self.index += 3

    def check_brackets(self, index):
        if self.expression[index] == ')':
            self.bracket_validator -= 1
            if self.bracket_validator < 0:
                raise Exception("Parse failed: improper bracket at index " + str(index))
            if len(self.expression) > index + 1 and self.expression[index + 1] not in [')', '+', '-', '*', '/']:
                self.tokens.append(Token(TokenValue.BRACKET_RIGHT, 0))
                self.tokens.append(Token(TokenValue.MULTIPLICATION, 0))
            else:
                self.tokens.append(Token(TokenValue.BRACKET_RIGHT, 0))
        elif self.expression[index] == '(':
            self.bracket_validator += 1
            if index > 0 and self.expression[index - 1] not in ['(', ')', '+', '-', '*', '/', 's', 'n','g']:
                self.tokens.append(Token(TokenValue.MULTIPLICATION, 0))
            self.tokens.append(Token(TokenValue.BRACKET_LEFT, 0))

    def check_x_neighbour(self, index):
        if index != 0 and self.tokens[len(self.tokens) - 1].token_value in [TokenValue.BRACKET_RIGHT, TokenValue.NONE]:
            self.tokens.append(Token(TokenValue.MULTIPLICATION, 0))
        self.tokens.append(Token(TokenValue.X, 0))
        self.index += 1

    def parse(self):
        while self.index < len(self.expression):
            current_char = self.expression[self.index]
            if current_char.isdigit():
                self.add_number(self.index)
                continue
            if current_char == 'c':
                try:
                    self.check_ctg_or_cos(self.index)
                except Exception as exc:
                    raise exc
                continue
            if current_char == 's':
                try:
                    self.check_sine(self.index)
                except Exception as exc:
                    raise exc
                continue
            if current_char == 't':
                try:
                    self.check_tg(self.index)
                except Exception as exc:
                    raise exc
                continue
            if current_char == 'l':
                try:
                    self.check_log(self.index)
                except Exception as exc:
                    raise exc
                continue
            if current_char == '^':
                self.tokens.append(Token(TokenValue.POWER, 0))
                self.index += 1
                continue
            if current_char == "\u221A":
                self.tokens.append(Token(TokenValue.ROOT, 0))
                self.index += 1
                continue
            if current_char == '(' or current_char == ')':
                try:
                    self.check_brackets(self.index)
                except Exception as exc:
                    raise exc
                self.index += 1
                continue
            else:
                token_symbol = self.other_symbols_map.get(current_char)
                if token_symbol is None:
                    raise Exception("Parse failed: improper symbol at index " + str(self.index))
                if token_symbol is TokenValue.X:
                    self.check_x_neighbour(self.index)
                else:
                    self.tokens.append(Token(token_symbol, 0))
                    self.index += 1

        if self.bracket_validator != 0:
            raise Exception("Parse failed: improper brackets")

        return self.tokens


