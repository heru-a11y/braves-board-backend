# type: ignore
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.task_repository import TaskRepository
from app.repositories.task_comment_repository import TaskCommentRepository
from app.schemas.task_comment_schemas import TaskCommentCreate
from app.exceptions.task_comment_exceptions import (
    TaskNotFoundException,
    CommentNotFoundException,
    CommentForbiddenException,
)
from app.constants import task_comment_messages


class TaskCommentService:
    @staticmethod
    async def add_comment(
        db: AsyncSession,
        task_id: uuid.UUID,
        content: str,
        current_user_id: uuid.UUID,
    ):
        task_repo = TaskRepository(db)
        task = await task_repo.get_by_id(task_id)
        if not task:
            raise TaskNotFoundException()

        comment_repo = TaskCommentRepository(db)
        comment_in = TaskCommentCreate(
            task_id=task_id,
            user_id=current_user_id,
            content=content,
        )
        comment = await comment_repo.create(comment_in)

        return {
            "id": comment.id,
            "user_id": comment.user_id,
            "content": comment.content,
            "created_at": comment.created_at,
        }

    @staticmethod
    async def delete_comment(
        db: AsyncSession,
        comment_id: uuid.UUID,
        current_user_id: uuid.UUID,
    ):
        comment_repo = TaskCommentRepository(db)
        comment = await comment_repo.get_by_id(comment_id)
        if not comment:
            raise CommentNotFoundException()

        if comment.user_id != current_user_id:
            raise CommentForbiddenException()

        await comment_repo.soft_delete(comment_id)
        return {"message": task_comment_messages.COMMENT_DELETED_SUCCESS}