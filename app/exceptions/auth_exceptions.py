from fastapi import status
from app.exceptions.base import CustomException
from app.constants import error_messages

class InvalidCredentialsException(CustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            message=error_messages.AUTH_INVALID_CREDENTIALS
        )

class TokenExpiredException(CustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            message=error_messages.AUTH_TOKEN_EXPIRED
        )

class GoogleAuthException(CustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=error_messages.AUTH_GOOGLE_FAILED
        )

class InvalidGoogleCodeException(CustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message=error_messages.AUTH_GOOGLE_CODE_INVALID
        )

class ForbiddenDomainException(CustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            message=error_messages.AUTH_FORBIDDEN_DOMAIN
        )