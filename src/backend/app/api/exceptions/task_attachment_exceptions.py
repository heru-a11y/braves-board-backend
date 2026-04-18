from fastapi import status
from app.api.exceptions.base_exceptions import CustomException

class InvalidFileTypeException(CustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Tipe file tidak didukung"
        )

class ImageTooLargeException(CustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Ukuran file gambar terlalu besar (Maksimal 10MB)"
        )

class PDFTooLargeException(CustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Ukuran file PDF terlalu besar (Maksimal 50MB)"
        )

class VideoTooLargeException(CustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Ukuran file video terlalu besar (Maksimal 1GB)"
        )

class AttachmentNotFoundException(CustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message="Lampiran tidak ditemukan"
        )