from fastapi import status # type: ignore

class AppException(Exception):
    """Base exception untuk seluruh error aplikasi."""
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message

class BadRequestError(AppException):
    """Status 400: Kesalahan logika bisnis atau parameter input."""
    def __init__(self, message: str = "Bad Request"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, message=message)

class UnauthorizedError(AppException):
    """Status 401: Token JWT tidak ditemukan, tidak valid, atau kedaluwarsa."""
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, message=message)

class ForbiddenError(AppException):
    """Status 403: Akses ditolak (domain email tidak valid / IDOR)."""
    def __init__(self, message: str = "Forbidden"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, message=message)

class NotFoundError(AppException):
    """Status 404: Sumber daya tidak ditemukan di database."""
    def __init__(self, message: str = "Not Found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, message=message)