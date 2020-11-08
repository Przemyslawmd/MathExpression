
from Token import Token


class Parser:

    def __init__(self, expression):

        self.expression = expression
        self.tokens = []
        self.bracket_validator = 0

        self.other_symbols_map = {
            '+': Token.PLUS,
            '-': Token.MINUS,
            '*': Token.MULTIPLICATION,
            '/': Token.DIVIDE,
            'x': Token.X
        }

    def add_digit(self, digit):
        switcher = {
            '0': Token.ZERO,
            '1': Token.ONE,
            '2': Token.TWO,
            '3': Token.THREE,
            '4': Token.FOUR,
            '5': Token.FIVE,
            '6': Token.SIX,
            '7': Token.SEVEN,
            '8': Token.EIGHT,
            '9': Token.NINE,
        }
        self.tokens.append(switcher.get(digit))

    def check_ctg_or_cos(self, index):
        if self.expression[index + 1] is 'o' and self.expression[index + 2] is 's':
            self.tokens.append(Token.COSINE)
        elif self.expression[index + 1] is 't' and self.expression[index + 2] is 'g':
            self.tokens.append(Token.COTANGENT)
        else:
            raise Exception("Parse expression failed: improper symbol at index " + str(index + 1) + " or " +
                            str(index + 2))

    def check_sin(self, index):
        if self.expression[index + 1] is 'i' and self.expression[index + 2] is 'n':
            self.tokens.append(Token.SINE)
        else:
            raise Exception("Parse expression failed: improper symbol at index: " + str(index + 1) + " or " +
                            str(index + 2))

    def check_tg(self, index):
        if self.expression[index + 1] is 'g':
            self.tokens.append(Token.TANGENT)
        else:
            raise Exception("Parse expression failed: improper symbol at index " + str(index + 1))

    def check_log(self, index):
        if self.expression[index + 1] is 'o' and self.expression[index + 2] is 'g':
            self.tokens.append(Token.LOG)
        else:
            raise Exception("Parse expression failed: improper symbol at index " + str(index + 1) + " or " +
                            str(index + 2))

    def check_brackets(self, index):
        if self.expression[index] is ')':
            self.bracket_validator -= 1
            if self.bracket_validator < 0:
                raise Exception("Parse expression failed: improper bracket at index " + str(index))
            self.tokens.append(Token.BRACKET_RIGHT)
        elif self.expression[index] is '(':
            self.bracket_validator += 1
            self.tokens.append(Token.BRACKET_LEFT)

    def parse(self):

        index = 0

        while index < len(self.expression):
            if self.expression[index] is ' ':
                index += 1
                continue
            if self.expression[index].isdigit():
                self.add_digit(self.expression[index])
                index += 1
                continue
            if self.expression[index] is 'c':
                try:
                    self.check_ctg_or_cos(index)
                except Exception as exc:
                    raise exc
                index += 3
                continue
            if self.expression[index] is 's':
                try:
                    self.check_sin(index)
                except Exception as exc:
                    raise exc
                index += 3
                continue
            if self.expression[index] is 't':
                try:
                    self.check_tg(index)
                except Exception as exc:
                    raise exc
                index += 2
                continue
            if self.expression[index] is 'l':
                try:
                    self.check_log(index)
                except Exception as exc:
                    raise exc
                index += 3
                continue
            if self.expression[index] is '^':
                self.tokens.append(Token.POWER)
                index += 1
                continue
            if self.expression[index] is "\u221A":
                self.tokens.append(Token.ROOT)
                index += 1
                continue
            if self.expression[index] is '(' or self.expression[index] is ')':
                try:
                    self.check_brackets(index)
                except Exception as exc:
                    raise exc
                index += 1
                continue

            Token.value = self.other_symbols_map.get(self.expression[index])
            if Token.value is None:
                raise Exception("Parse expression failed: improper symbol at index " + str(index))
            self.tokens.append(Token.value)
            index += 1

        if self.bracket_validator is not 0:
            raise Exception("Parse expression failed: improper brackets")

        return self.tokens

