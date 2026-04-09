from fastapi import status
from app.exceptions.base import CustomException
from app.constants import auth_messages

class InvalidCredentialsException(CustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            message=auth_messages.INVALID_CREDENTIALS
        )

class TokenExpiredException(CustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            message=auth_messages.TOKEN_EXPIRED
        )

class InvalidTokenException(CustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message=auth_messages.TOKEN_INVALID
        )

class GoogleAuthException(CustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=auth_messages.GOOGLE_FAILED
        )

class InvalidGoogleCodeException(CustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message=auth_messages.GOOGLE_CODE_INVALID
        )

class ForbiddenDomainException(CustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            message=auth_messages.FORBIDDEN_DOMAIN
        )

class InvalidRefreshTokenException(CustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message=auth_messages.REFRESH_TOKEN_INVALID
        )