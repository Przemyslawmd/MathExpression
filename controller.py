
from postfix.calculator import calculate
from postfix.postfix import Postfix
from tokens.parser import Parser


def calculate_values(expression, x_min, x_max, x_precision) -> list or None:
    if not expression:
        return None
    tokens = Parser(expression).parse()
    if tokens is None:
        return None

    postfix = Postfix().create_postfix(tokens)
    result = calculate(postfix, x_min, x_max, x_precision)
    return result


