from fastapi import status
from app.api.exceptions.base_exceptions import CustomException


class BoardNotFoundException(CustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message="Board tidak ditemukan",
        )


class InvalidBoardUpdateException(CustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Data pembaruan board tidak valid",
        )