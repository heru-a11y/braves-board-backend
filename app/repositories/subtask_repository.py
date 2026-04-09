import uuid
from datetime import datetime, timezone
from typing import Sequence
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.subtask import Subtask
from app.schemas.subtask import SubtaskCreate

class SubtaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, subtask_id: uuid.UUID) -> Subtask | None:
        stmt = select(Subtask).where(Subtask.id == subtask_id, Subtask.deleted_at.is_(None))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all_by_task_id(self, task_id: uuid.UUID) -> Sequence[Subtask]:
        stmt = select(Subtask).where(Subtask.task_id == task_id, Subtask.deleted_at.is_(None)).order_by(Subtask.position)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, subtask_in: SubtaskCreate) -> Subtask:
        db_subtask = Subtask(**subtask_in.model_dump())
        self.session.add(db_subtask)
        await self.session.commit()
        await self.session.refresh(db_subtask)
        return db_subtask

    async def update(self, subtask_id: uuid.UUID, update_data: dict) -> Subtask | None:
        stmt = (
            update(Subtask)
            .where(Subtask.id == subtask_id, Subtask.deleted_at.is_(None))
            .values(**update_data, updated_at=datetime.now(timezone.utc))
            .returning(Subtask)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one_or_none()

    async def soft_delete(self, subtask_id: uuid.UUID) -> bool:
        stmt = (
            update(Subtask)
            .where(Subtask.id == subtask_id, Subtask.deleted_at.is_(None))
            .values(deleted_at=datetime.now(timezone.utc))
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0