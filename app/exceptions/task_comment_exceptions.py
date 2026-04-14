from fastapi import status
from app.exceptions.base import CustomException
from app.constants import task_comment_messages


class TaskNotFoundException(CustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message=task_comment_messages.TASK_NOT_FOUND
        )


class CommentNotFoundException(CustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message=task_comment_messages.COMMENT_NOT_FOUND
        )


class CommentForbiddenException(CustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            message=task_comment_messages.COMMENT_FORBIDDEN
        )