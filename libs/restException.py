class RestException(Exception):
    statusCode = 500

    def __init__(self, message, statusCode):
        self.message = message
        self.statusCode = statusCode

    def __str__(self):
        return str(self.statusCode) + ': ' + repr(self.message)
