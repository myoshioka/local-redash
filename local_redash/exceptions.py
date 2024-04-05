class AuthenticationError(Exception):

    def __init__(self) -> None:
        message = 'Authentication error: API key is incorrect or not specified.'
        super().__init__(message)
