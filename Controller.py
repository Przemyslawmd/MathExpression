
from Notations.Postfix import Postfix
from Notations.Calculator import Calculator
from Token.Parser import Parser


class Controller:

    @staticmethod
    def calculate_values(expression, x_min, x_max, x_precision):
        try:
            tokens = Parser(expression).parse()
        except Exception as e:
            raise Exception(e)

        postfix = Postfix().create_postfix(tokens)
        try:
            result = Calculator().calculate(postfix, x_min, x_max, x_precision)
        except Exception as e:
            raise Exception(e)
        return result


