from fastapi import status
from app.api.exceptions.base_exceptions import CustomException


class ColumnNotFoundException(CustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message="Kolom tidak ditemukan",
        )


class InvalidColumnPositionException(CustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Posisi kolom tidak valid",
        )