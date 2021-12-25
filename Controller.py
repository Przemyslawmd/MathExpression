
from Notations.Postfix import Postfix
from Tokens.Parser import Parser


class Controller:

    def calculate_values(self, expression, x_min, x_max):
        try:
            tokens = Parser(expression).parse()
        except Exception as e:
            raise Exception(e)

        postfix = Postfix()
        postfix.create_postfix(tokens)
        result = postfix.calculate(x_min, x_max)
        return result

