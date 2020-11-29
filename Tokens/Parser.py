
from Tokens.Token import Token, TokenValue


class Parser:

    def __init__(self, expression):

        self.expression = expression.replace(" ",'')
        self.tokens = []
        self.bracket_validator = 0

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
        return shift


    def check_ctg_or_cos(self, index):
        if self.expression[index + 1] is 'o' and self.expression[index + 2] is 's':
            self.tokens.append(Token(TokenValue.COSINE, 0))
        elif self.expression[index + 1] is 't' and self.expression[index + 2] is 'g':
            self.tokens.append(Token(TokenValue.COTANGENT, 0))
        else:
            raise Exception("Parse failed: improper symbol at index " + str(index + 1) + " or " + str(index + 2))


    def check_sine(self, index):
        if self.expression[index + 1] is 'i' and self.expression[index + 2] is 'n':
            self.tokens.append(Token(TokenValue.SINE, 0))
        else:
            raise Exception("Parse failed: improper symbol at index: " + str(index + 1) + " or " + str(index + 2))


    def check_tg(self, index):
        if self.expression[index + 1] is 'g':
            self.tokens.append(Token(TokenValue.TANGENT, 0))
        else:
            raise Exception("Parse failed: improper symbol at index " + str(index + 1))


    def check_log(self, index):
        if self.expression[index + 1] is 'o' and self.expression[index + 2] is 'g':
            self.tokens.append(Token(TokenValue.LOG, 0))
        else:
            raise Exception("Parse failed: improper symbol at index " + str(index + 1) + " or " + str(index + 2))


    def check_brackets(self, index):
        if self.expression[index] is ')':
            self.bracket_validator -= 1
            if self.bracket_validator < 0:
                raise Exception("Parse failed: improper bracket at index " + str(index))
            if len(self.expression) > index + 1 and self.expression[index + 1] not in [')', '+', '-', '*', '/']:
                self.tokens.append(Token(TokenValue.BRACKET_RIGHT, 0))
                self.tokens.append(Token(TokenValue.MULTIPLICATION, 0))
            else:
                self.tokens.append(Token(TokenValue.BRACKET_RIGHT, 0))
        elif self.expression[index] is '(':
            self.bracket_validator += 1
            if index > 0 and self.expression[index - 1] not in ['(', ')', '+', '-', '*', '/', 's', 'n','g']:
                self.tokens.append(Token(TokenValue.MULTIPLICATION, 0))
            self.tokens.append(Token(TokenValue.BRACKET_LEFT, 0))


    def parse(self):
        index = 0
        while index < len(self.expression):
            current_char = self.expression[index]
            if current_char.isdigit():
                index += self.add_number(index)
                continue
            if current_char is 'c':
                try:
                    self.check_ctg_or_cos(index)
                except Exception as exc:
                    raise exc
                index += 3
                continue
            if current_char is 's':
                try:
                    self.check_sine(index)
                except Exception as exc:
                    raise exc
                index += 3
                continue
            if current_char is 't':
                try:
                    self.check_tg(index)
                except Exception as exc:
                    raise exc
                index += 2
                continue
            if current_char is 'l':
                try:
                    self.check_log(index)
                except Exception as exc:
                    raise exc
                index += 3
                continue
            if current_char is '^':
                self.tokens.append(Token(TokenValue.POWER, 0))
                index += 1
                continue
            if current_char is "\u221A":
                self.tokens.append(Token(TokenValue.ROOT, 0))
                index += 1
                continue
            if current_char is '(' or current_char is ')':
                try:
                    self.check_brackets(index)
                except Exception as exc:
                    raise exc
                index += 1
                continue
            else:
                token_symbol = self.other_symbols_map.get(current_char)
                if token_symbol is None:
                    raise Exception("Parse failed: improper symbol at index " + str(index))
                self.tokens.append(Token(token_symbol, 0))
                index += 1

        if self.bracket_validator is not 0:
            raise Exception("Parse failed: improper brackets")

        return self.tokens


