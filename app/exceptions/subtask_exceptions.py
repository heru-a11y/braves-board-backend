from fastapi import status
from app.exceptions.base import CustomException
from app.constants import subtask_messages

class SubtaskNotFoundException(CustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message=subtask_messages.SUBTASK_NOT_FOUND
        )