
from numpy import arange

from errors import Error
from errorStorage import ErrorStorage
from postfix.calculator import calculate
from postfix.postfix import Postfix
from tree.tree import create_tree
from tokens.parser import Parser
from tokens.token import TokenType


def calculate_values(expression, x_min, x_max, precision) -> list or None:
    if not expression:
        return None
    tokens = Parser(expression).parse()
    if tokens is None:
        return None

    postfix = Postfix().create_postfix(tokens)
    if len(postfix) == 1:
        return fill_values(x_min, x_max, precision, postfix[0])

    root = create_tree(postfix)
    division_or_tangent = filter(lambda t: t.type is TokenType.DIVISION or t.type is TokenType.TANGENT, tokens)
    continuity = any(division_or_tangent)
    result = calculate(root, x_min, x_max, precision, continuity)
    return result

# ------------------------------- INTERNAL ----------------------------------- #

def fill_values(x_min, x_max, precision, token) -> list or None:
    data = arange(x_min, x_max + precision, precision)
    if token.type is TokenType.X:
        return data
    if token.type is TokenType.NUMBER:
        data.fill(token.data)
        return data
    ErrorStorage.put_error(Error.INTERNAL_EXCEPTION_SINGLE_TOKEN)
    return None

