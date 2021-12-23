
from Tokens.Token import Token, TokenValue
from Tokens.TokenUtils import TokenUtils


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
        self.tokens.append(Token(TokenValue.NUMBER, number))
        self.index += shift


    def check_ctg_or_cos(self, index):
        if self.expression[index + 1] == 'o' and self.expression[index + 2] == 's':
            self.tokens.append(Token(TokenValue.COSINE))
        elif self.expression[index + 1] == 't' and self.expression[index + 2] == 'g':
            self.tokens.append(Token(TokenValue.COTANGENT))
        else:
            raise Exception("Parse failed: improper symbol at index " + str(index + 1) + " or " + str(index + 2))
        self.index += 3


    def check_sine(self, index):
        if self.expression[index + 1] == 'i' and self.expression[index + 2] == 'n':
            self.tokens.append(Token(TokenValue.SINE))
        else:
            raise Exception("Parse failed: improper symbol at index: " + str(index + 1) + " or " + str(index + 2))
        self.index += 3


    def check_tg(self, index):
        if self.expression[index + 1] == 'g':
            self.tokens.append(Token(TokenValue.TANGENT))
        else:
            raise Exception("Parse failed: improper symbol at index " + str(index + 1))
        self.index += 2


    def check_log(self, index):
        if self.expression[index + 1] == 'o' and self.expression[index + 2] == 'g':
            self.tokens.append(Token(TokenValue.LOG))
        else:
            raise Exception("Parse failed: improper symbol at index " + str(index + 1) + " or " + str(index + 2))
        self.index += 3


    def check_brackets(self, index):
        if self.expression[index] == ')':
            self.bracket_validator -= 1
            if self.bracket_validator < 0:
                raise Exception("Parse failed: improper bracket at index " + str(index))
            if len(self.expression) > index + 1 and self.expression[index + 1] not in [')', '+', '-', '*', '/']:
                self.tokens.append(Token(TokenValue.BRACKET_RIGHT))
                self.tokens.append(Token(TokenValue.MULTIPLICATION))
            else:
                self.tokens.append(Token(TokenValue.BRACKET_RIGHT))
        elif self.expression[index] == '(':
            self.bracket_validator += 1
            if index > 0 and self.expression[index - 1] not in ['(', ')', '+', '-', '*', '/', 's', 'n','g']:
                self.tokens.append(Token(TokenValue.MULTIPLICATION))
            self.tokens.append(Token(TokenValue.BRACKET_LEFT))


    def check_negative(self, index):
        if index == 0 or self.tokens[len(self.tokens) - 1].token_value in [TokenValue.BRACKET_LEFT,
                                                                           TokenValue.MULTIPLICATION,
                                                                           TokenValue.DIVISION,
                                                                           TokenValue.PLUS]:
            self.tokens.append(Token(TokenValue.NEGATIVE))
        elif index == len(self.expression) - 1 or self.expression[index + 1] in [')', '*', '/']:
            raise Exception("Parse failed: improper usage of negative symbol")
        else:
            self.tokens.append(Token(TokenValue.MINUS))
        self.index += 1


    def add_multiplication(self):
        indices = []
        for index, token in enumerate(self.tokens):
            if token.token_value in [TokenValue.BRACKET_RIGHT, TokenValue.NUMBER, TokenValue.X] and index <= (len(self.tokens) - 2) and \
                    (self.tokens[index + 1].token_value in [TokenValue.X, TokenValue.NUMBER, TokenValue.BRACKET_LEFT] or self.tokens[index + 1].token_value in TokenUtils.trigonometry):
                    indices.append(index + 1)

        index_shift = 0
        for index in indices:
            self.tokens.insert(index + index_shift, Token(TokenValue.MULTIPLICATION))
            index_shift += 1


    def remove_negative_tokens(self):
        is_current_token_negative = False
        for index, token in enumerate(self.tokens):
            if token.token_value is TokenValue.NEGATIVE:
                is_current_token_negative = True
                continue
            if is_current_token_negative:
                if token.token_value is TokenValue.NUMBER:
                    number = token.token_number
                    self.tokens[index] = Token(TokenValue.NUMBER, number * -1)
                elif token.token_value is TokenValue.X:
                    self.tokens[index] = Token(TokenValue.X_NEGATIVE)
                else:
                    raise Exception("Parse failed: improper usage of negative symbol")
                is_current_token_negative = False

        for i in range(len(self.tokens) - 1, -1, -1):
            if self.tokens[i].token_value is TokenValue.NEGATIVE:
                del self.tokens[i]


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
                self.tokens.append(Token(TokenValue.POWER))
                self.index += 1
                continue
            if current_char == "\u221A":
                self.tokens.append(Token(TokenValue.ROOT))
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
                elif token_symbol is TokenValue.X:
                    self.tokens.append(Token(TokenValue.X))
                    self.index += 1
                elif token_symbol is TokenValue.MINUS:
                    try:
                        self.check_negative(self.index)
                    except Exception as e:
                        raise Exception(e)
                else:
                    self.tokens.append(Token(token_symbol))
                    self.index += 1

        if self.bracket_validator != 0:
            raise Exception("Parse failed: improper brackets")

        self.add_multiplication()

        try:
            self.remove_negative_tokens()
        except Exception as e:
            raise Exception(e)

        return self.tokens


