import uuid
from datetime import datetime, timezone
from typing import Sequence
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.task import Task
from app.schemas.task import TaskCreate

class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, task_id: uuid.UUID) -> Task | None:
        stmt = select(Task).where(Task.id == task_id, Task.deleted_at.is_(None))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all_by_column_id(self, column_id: uuid.UUID) -> Sequence[Task]:
        stmt = select(Task).where(Task.column_id == column_id, Task.deleted_at.is_(None)).order_by(Task.position)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, task_in: TaskCreate) -> Task:
        db_task = Task(**task_in.model_dump())
        self.session.add(db_task)
        await self.session.commit()
        await self.session.refresh(db_task)
        return db_task

    async def update(self, task_id: uuid.UUID, update_data: dict) -> Task | None:
        stmt = (
            update(Task)
            .where(Task.id == task_id, Task.deleted_at.is_(None))
            .values(**update_data, updated_at=datetime.now(timezone.utc))
            .returning(Task)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one_or_none()

    async def soft_delete(self, task_id: uuid.UUID) -> bool:
        stmt = (
            update(Task)
            .where(Task.id == task_id, Task.deleted_at.is_(None))
            .values(deleted_at=datetime.now(timezone.utc))
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0