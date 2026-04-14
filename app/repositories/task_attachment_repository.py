import uuid
from typing import Sequence
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.task_attachment_model import TaskAttachment
from app.schemas.task_attachment_schemas import TaskAttachmentCreate

class TaskAttachmentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, attachment_id: uuid.UUID) -> TaskAttachment | None:
        stmt = select(TaskAttachment).where(TaskAttachment.id == attachment_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all_by_task_id(self, task_id: uuid.UUID) -> Sequence[TaskAttachment]:
        stmt = select(TaskAttachment).where(TaskAttachment.task_id == task_id).order_by(TaskAttachment.uploaded_at)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, attachment_in: TaskAttachmentCreate) -> TaskAttachment:
        db_attachment = TaskAttachment(**attachment_in.model_dump())
        self.session.add(db_attachment)
        await self.session.commit()
        await self.session.refresh(db_attachment)
        return db_attachment

    async def delete(self, attachment_id: uuid.UUID) -> bool:
        stmt = delete(TaskAttachment).where(TaskAttachment.id == attachment_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0