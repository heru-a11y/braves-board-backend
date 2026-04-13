import uuid
from datetime import datetime, timezone
from typing import Sequence
from sqlalchemy import select, update, func
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
        stmt = (
            select(Subtask)
            .where(Subtask.task_id == task_id, Subtask.deleted_at.is_(None))
            .order_by(Subtask.position)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_max_position(self, task_id: uuid.UUID) -> int:
        stmt = select(func.max(Subtask.position)).where(
            Subtask.task_id == task_id,
            Subtask.deleted_at.is_(None)
        )
        result = await self.session.execute(stmt)
        max_pos = result.scalar()
        return max_pos if max_pos is not None else 0

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

    async def shift_positions(
        self,
        task_id: uuid.UUID,
        from_position: int,
        to_position: int,
        shift: int
    ) -> None:
        """
        Geser posisi subtask lain dalam rentang [from_position, to_position]
        shift: +1 (turun) atau -1 (naik)
        """
        stmt = (
            update(Subtask)
            .where(
                Subtask.task_id == task_id,
                Subtask.deleted_at.is_(None),
                Subtask.position >= from_position,
                Subtask.position <= to_position,
            )
            .values(
                position=Subtask.position + shift,
                updated_at=datetime.now(timezone.utc)
            )
        )
        await self.session.execute(stmt)

    async def soft_delete(self, subtask_id: uuid.UUID) -> bool:
        stmt = (
            update(Subtask)
            .where(Subtask.id == subtask_id, Subtask.deleted_at.is_(None))
            .values(deleted_at=datetime.now(timezone.utc))
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0