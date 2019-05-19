

class StandardException(Exception):
    def __init__(self, message, code=None):
        self.message = message
        self.code = code


class ClientException(StandardException):
    pass


class ValidationException(ClientException):
    pass


class AuthNotFoundException(ValidationException):
    pass


class ServerException(StandardException):
    pass
