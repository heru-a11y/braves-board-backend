from fastapi import status
from app.exceptions.base import CustomException
from app.constants import subtask_messages

class SubtaskNotFoundException(CustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message=subtask_messages.SUBTASK_NOT_FOUND
        )

class NoSubtaskFieldsToUpdateException(CustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=subtask_messages.SUBTASK_NO_FIELDS_TO_UPDATE
        )

class InvalidSubtaskPositionException(CustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=subtask_messages.SUBTASK_INVALID_POSITION
        )

class InvalidSubtaskStatusException(CustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=subtask_messages.SUBTASK_INVALID_STATUS
        )