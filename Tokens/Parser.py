
from Tokens.Token import Token, TokenValue
from Tokens.TokenUtils import TokenUtils


class Parser:

    def __init__(self, expression):
        self.__expression = expression.replace(" ", '')
        self.__tokens = []
        self.__bracket_validator = 0
        self.__index = 0

        self.one_char_tokens = {
            '+': TokenValue.PLUS,
            '-': TokenValue.MINUS,
            '*': TokenValue.MULTIPLICATION,
            '/': TokenValue.DIVISION,
            'x': TokenValue.X,
            '^': TokenValue.POWER
        }

        self.three_chars_tokens = {
            'cos': TokenValue.COSINE,
            'ctg': TokenValue.COTANGENT,
            'log': TokenValue.LOG,
            'sin': TokenValue.SINE,
        }


    def add_number(self):
        number = int(self.__expression[self.__index], 16)
        shift = 1
        while (self.__index + shift) < len(self.__expression) and self.__expression[self.__index + shift].isdigit():
            number = number * 10 + int(self.__expression[self.__index + shift])
            shift += 1
        self.__tokens.append(Token(TokenValue.NUMBER, number))
        self.__index += shift


    def check_multiple_char_token(self):
        expression_len = len(self.__expression)
        index = self.__index
        if expression_len - index >= 2 and self.__expression[index: index + 2] == 'tg':
            self.__tokens.append(Token(TokenValue.TANGENT))
            self.__index += 2
            return
        if expression_len - index >= 3:
            sub_str = self.__expression[index: index + 3]
            if sub_str in self.three_chars_tokens.keys():
                self.__tokens.append(Token(self.three_chars_tokens.get(sub_str)))
                self.__index += 3
                return
        if expression_len - index >= 4 and self.__expression[index: index + 4] == 'sqrt':
            self.__tokens.append(Token(TokenValue.ROOT))
            self.__index += 4
        else:
            raise Exception(f"Parser error: improper symbol between numbers {index + 1} and {index + 4}")


    def check_brackets(self, current_char):
        if current_char == ')':
            self.__bracket_validator -= 1
            if self.__bracket_validator < 0:
                return False
            self.__tokens.append(Token(TokenValue.BRACKET_RIGHT))
        else:
            self.__bracket_validator += 1
            self.__tokens.append(Token(TokenValue.BRACKET_LEFT))
        self.__index += 1
        return True


    def check_negative(self):
        if self.__index == 0 or self.__tokens[len(self.__tokens) - 1].value in [TokenValue.BRACKET_LEFT,
                                                                                TokenValue.MULTIPLICATION,
                                                                                TokenValue.DIVISION,
                                                                                TokenValue.PLUS]:
            self.__tokens.append(Token(TokenValue.NEGATIVE))
        elif self.__index == len(self.__expression) - 1 or self.__expression[self.__index + 1] in [')', '*', '/']:
            raise Exception("Parser error: improper usage of negative symbol")
        else:
            self.__tokens.append(Token(TokenValue.MINUS))
        self.__index += 1


    def add_multiplication(self):
        indices = []
        for index, token in enumerate(self.__tokens[:-1]):
            if token.value in [TokenValue.BRACKET_RIGHT, TokenValue.X, TokenValue.NUMBER]:
                next_token = self.__tokens[index + 1]
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
            self.__tokens.insert(index + index_shift, Token(TokenValue.MULTIPLICATION))
            index_shift += 1


    def remove_negative_tokens(self):
        is_current_token_negative = False
        for index, token in enumerate(self.__tokens):
            if token.value is TokenValue.NEGATIVE:
                is_current_token_negative = True
                continue
            if is_current_token_negative:
                if token.value is TokenValue.NUMBER:
                    number = token.number
                    self.__tokens[index] = Token(TokenValue.NUMBER, number * -1)
                elif token.value is TokenValue.X:
                    self.__tokens[index] = Token(TokenValue.X_NEGATIVE)
                else:
                    raise Exception("Parser error: improper usage of negative symbol")
                is_current_token_negative = False

        for i in range(len(self.__tokens) - 1, -1, -1):
            if self.__tokens[i].value is TokenValue.NEGATIVE:
                del self.__tokens[i]


    def parse(self):
        while self.__index < len(self.__expression):
            current_char = self.__expression[self.__index]
            if current_char.isdigit():
                self.add_number()
                continue
            if current_char in ['c', 's', 'l', 't']:
                try:
                    self.check_multiple_char_token()
                except Exception as exc:
                    raise exc
                continue
            if current_char == '(' or current_char == ')':
                if not self.check_brackets(current_char):
                    raise Exception(f"Parser error: improper bracket at number {self.__index + 1}")
                continue
            else:
                token_symbol = self.one_char_tokens.get(current_char)
                if token_symbol is None:
                    raise Exception(f'Parser error: improper symbol at number {self.__index + 1}')
                elif token_symbol is TokenValue.MINUS:
                    try:
                        self.check_negative()
                    except Exception as e:
                        raise Exception(e)
                else:
                    self.__tokens.append(Token(token_symbol))
                    self.__index += 1

        if self.__bracket_validator != 0:
            raise Exception("Parser error: improper brackets")

        self.add_multiplication()

        try:
            self.remove_negative_tokens()
        except Exception as e:
            raise Exception(e)

        return self.__tokens


