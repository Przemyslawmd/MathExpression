
from Notations.Postfix import Postfix
from Tokens.Parser import Parser


class Controller:

    @staticmethod
    def calculate_values(expression, x_min, x_max, x_precision):
        try:
            tokens = Parser(expression).parse()
        except Exception as e:
            raise Exception(e)

        postfix = Postfix()
        postfix.create_postfix(tokens)
        try:
            result = postfix.calculate(x_min, x_max, x_precision)
        except Exception as e:
            raise Exception(e)
        return result


