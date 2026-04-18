import uuid
from typing import Sequence
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.time_log_model import TimeLog
from app.api.time_tracking.schema import TimeLogCreate


class TimeLogRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, log_id: uuid.UUID) -> TimeLog | None:
        stmt = select(TimeLog).where(TimeLog.id == log_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all_by_task_id(self, task_id: uuid.UUID) -> Sequence[TimeLog]:
        stmt = select(TimeLog).where(TimeLog.task_id == task_id).order_by(TimeLog.created_at)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, log_in: TimeLogCreate) -> TimeLog:
        db_log = TimeLog(**log_in.model_dump())
        self.session.add(db_log)
        await self.session.commit()
        await self.session.refresh(db_log)
        return db_log

    async def update(self, log_id: uuid.UUID, update_data: dict) -> TimeLog | None:
        stmt = (
            update(TimeLog)
            .where(TimeLog.id == log_id)
            .values(**update_data)
            .returning(TimeLog)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one_or_none()