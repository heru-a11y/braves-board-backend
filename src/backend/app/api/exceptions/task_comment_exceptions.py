from fastapi import status
from app.api.exceptions.base_exceptions import CustomException

class CommentNotFoundException(CustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message="Komentar tidak ditemukan"
        )

class CommentForbiddenException(CustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            message="Anda tidak memiliki akses untuk menghapus komentar ini"
        )