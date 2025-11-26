
from errors import Error
from errorStorage import ErrorStorage
from postfix.calculator import calculate
from postfix.postfix import Postfix
from tree.tree import create_tree
from tokens.parser import Parser
from tokens.token import TokenType


def calculate_values(expression, x_values) -> list | None:
    if not expression:
        return None
    tokens = Parser(expression).parse()
    if tokens is None:
        return None

    postfix = Postfix().create_postfix(tokens)
    if len(postfix) == 1:
        return fill_values(x_values, postfix[0])

    root = create_tree(postfix)
    division_or_tangent = filter(lambda t: t.type is TokenType.DIVISION or t.type is TokenType.TANGENT, postfix)
    check_continuity = any(division_or_tangent)
    result = calculate(root, x_values, check_continuity)
    return result

# ------------------------------- INTERNAL ----------------------------------- #

def fill_values(x_values, token) -> list | None:
    if token.type is TokenType.X:
        return x_values
    if token.type is TokenType.NUMBER:
        x_values.fill(token.data)
        return x_values
    ErrorStorage.put_error(Error.INTERNAL_EXCEPTION_SINGLE_TOKEN)
    return None

