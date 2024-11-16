
from numpy import arange

from postfix.calculator import calculate
from postfix.postfix import Postfix
from tokens.parser import Parser
from tokens.token import TokenType


def calculate_values(expression, x_min, x_max, precision) -> list or None:
    if not expression:
        return None
    tokens = Parser(expression).parse()
    if tokens is None:
        return None
    if len(tokens) == 1:
        return fill_values(x_min, x_max, precision, tokens[0])

    postfix = Postfix().create_postfix(tokens)
    result = calculate(postfix, x_min, x_max, precision)
    return result

# ------------------------------- INTERNAL ----------------------------------- #

def fill_values(x_min, x_max, precision, token) -> list or None:
    if token.type is TokenType.X:
        return arange(x_min, x_max + precision, precision)
    if token.type is TokenType.NUMBER:
        data = arange(x_min, x_max + precision, precision)
        data.fill(token.data)
        return data
    return None

