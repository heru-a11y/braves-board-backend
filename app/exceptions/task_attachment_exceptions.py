from fastapi import status
from app.exceptions.base import CustomException
from app.constants import task_attachment_messages

class InvalidFileTypeException(CustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=task_attachment_messages.INVALID_FILE_TYPE
        )

class ImageTooLargeException(CustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=task_attachment_messages.FILE_TOO_LARGE_IMAGE
        )

class PDFTooLargeException(CustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=task_attachment_messages.FILE_TOO_LARGE_PDF
        )

class VideoTooLargeException(CustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=task_attachment_messages.FILE_TOO_LARGE_VIDEO
        )