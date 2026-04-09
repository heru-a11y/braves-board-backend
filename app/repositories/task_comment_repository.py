import uuid
from datetime import datetime, timezone
from typing import Sequence
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.task_comment import TaskComment
from app.schemas.task_comment import TaskCommentCreate

class TaskCommentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, comment_id: uuid.UUID) -> TaskComment | None:
        stmt = select(TaskComment).where(TaskComment.id == comment_id, TaskComment.deleted_at.is_(None))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all_by_task_id(self, task_id: uuid.UUID) -> Sequence[TaskComment]:
        stmt = select(TaskComment).where(TaskComment.task_id == task_id, TaskComment.deleted_at.is_(None)).order_by(TaskComment.created_at)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, comment_in: TaskCommentCreate) -> TaskComment:
        db_comment = TaskComment(**comment_in.model_dump())
        self.session.add(db_comment)
        await self.session.commit()
        await self.session.refresh(db_comment)
        return db_comment

    async def update(self, comment_id: uuid.UUID, update_data: dict) -> TaskComment | None:
        stmt = (
            update(TaskComment)
            .where(TaskComment.id == comment_id, TaskComment.deleted_at.is_(None))
            .values(**update_data, updated_at=datetime.now(timezone.utc))
            .returning(TaskComment)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one_or_none()

    async def soft_delete(self, comment_id: uuid.UUID) -> bool:
        stmt = (
            update(TaskComment)
            .where(TaskComment.id == comment_id, TaskComment.deleted_at.is_(None))
            .values(deleted_at=datetime.now(timezone.utc))
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0