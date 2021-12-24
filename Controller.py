
from Notations.Postfix import Postfix
from Tokens.Parser import Parser


class Controller:

    def calculate_values(self, expression):
        try:
            tokens = Parser(expression).parse()
        except Exception as e:
            raise Exception(e)

        postfix = Postfix()
        postfix.create_postfix(tokens)
        result = postfix.calculate(0, 10)
        return result

