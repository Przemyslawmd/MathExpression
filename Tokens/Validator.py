
from Tokens.Token import TokenValue
from Tokens.TokenUtils import TokenUtils
from Errors import ErrorType, ErrorMessage


class Validator:

    def __init__(self):
        self.filter = [TokenValue.X, TokenValue.NUMBER, TokenValue.BRACKET_LEFT]

    def validate(self, tokens):
        for index, token in enumerate(tokens):
            if token.value is TokenValue.LOG:
                if not tokens[index + 1] or tokens[index + 1].value not in self.filter:
                    raise Exception(ErrorMessage[ErrorType.VALIDATOR_LOGARITHM])
            if token.value is TokenValue.ROOT:
                if not tokens[index + 1] or tokens[index + 1].value not in self.filter:
                    raise Exception(ErrorMessage[ErrorType.VALIDATOR_ROOT])
            if token.value in TokenUtils.trigonometry:
                if not tokens[index + 1] or tokens[index + 1].value not in self.filter:
                    raise Exception(ErrorMessage[ErrorType.VALIDATOR_TRIGONOMETRY])

