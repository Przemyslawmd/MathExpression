
from Tokens.Token import TokenType
from Tokens.TokenUtils import TokenUtils
from Errors import ErrorType, ErrorMessage


class Validator:

    def __init__(self):
        self.filter_positive = [TokenType.X, TokenType.NUMBER, TokenType.BRACKET_LEFT]
        self.filter_negative = TokenUtils.basic_arithmetic + [TokenType.BRACKET_RIGHT]

    def validate(self, tokens):
        last = len(tokens) - 1
        for index, token in enumerate(tokens):
            if token.type is TokenType.LOG:
                if not tokens[index + 1] or tokens[index + 1].type not in self.filter_positive:
                    raise Exception(ErrorMessage[ErrorType.VALIDATOR_LOGARITHM])
            if token.type is TokenType.POWER:
                if not tokens[index + 1] or tokens[index + 1].type not in self.filter_positive:
                    raise Exception(ErrorMessage[ErrorType.VALIDATOR_POWER])
            if token.type is TokenType.ROOT:
                if not tokens[index + 1] or tokens[index + 1].type not in self.filter_positive:
                    raise Exception(ErrorMessage[ErrorType.VALIDATOR_ROOT])
            if token.type in TokenUtils.trigonometry:
                if not tokens[index + 1] or tokens[index + 1].type not in self.filter_positive:
                    raise Exception(ErrorMessage[ErrorType.VALIDATOR_TRIGONOMETRY])
            if token.type in TokenUtils.basic_arithmetic:
                if not tokens[index + 1] or tokens[index + 1].type in self.filter_negative:
                    raise Exception(ErrorMessage[ErrorType.VALIDATOR_BASIC_ARITHMETIC])
            if token.type is TokenType.NUMBER:
                if index != last and tokens[index + 1].type is TokenType.NUMBER:
                    raise Exception(ErrorMessage[ErrorType.VALIDATOR_NUMBER])


