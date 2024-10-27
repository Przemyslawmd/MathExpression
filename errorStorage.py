
class ErrorStorage:

    errors = []

    @staticmethod
    def putError(error):
        ErrorStorage.errors.append(error)


    @staticmethod
    def getErrors():
        return ErrorStorage.errors


    @staticmethod
    def clear():
        ErrorStorage.errors.clear()

