from fastapi import status
from app.exceptions.base import CustomException
from app.constants import task_messages

class ColumnNotFoundException(CustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message=task_messages.COLUMN_NOT_FOUND
        )

class TaskNotFoundException(CustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message=task_messages.TASK_NOT_FOUND
        )