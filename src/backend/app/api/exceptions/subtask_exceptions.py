from fastapi import status
from app.api.exceptions.base_exceptions import CustomException


class SubtaskNotFoundException(CustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message="Subtask tidak ditemukan",
        )


class NoSubtaskFieldsToUpdateException(CustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Tidak ada data subtask yang diperbarui",
        )


class InvalidSubtaskPositionException(CustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Posisi subtask tidak valid",
        )


class InvalidSubtaskStatusException(CustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Status penyelesaian subtask tidak valid",
        )