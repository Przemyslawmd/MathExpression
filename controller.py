
from postfix.calculator import calculate
from postfix.postfix import Postfix
from tokens.parser import Parser


def calculate_values(expression, x_min, x_max, x_precision):
    try:
        tokens = Parser(expression).parse()
    except Exception as e:
        raise Exception(e)

    postfix = Postfix().create_postfix(tokens)
    try:
        result = calculate(postfix, x_min, x_max, x_precision)
    except Exception as e:
        raise Exception(e)
    return result


