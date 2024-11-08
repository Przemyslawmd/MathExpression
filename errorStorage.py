
class ErrorStorage:

    errors = []

    @staticmethod
    def put_error(error):
        ErrorStorage.errors.append(error)


    @staticmethod
    def get_errors():
        return ErrorStorage.errors


    @staticmethod
    def clear():
        ErrorStorage.errors.clear()

