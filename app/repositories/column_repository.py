import uuid
from datetime import datetime, timezone
from typing import Sequence
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.column import Column
from app.schemas.column import ColumnCreate

class ColumnRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, column_id: uuid.UUID) -> Column | None:
        stmt = select(Column).where(Column.id == column_id, Column.deleted_at.is_(None))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all_by_board_id(self, board_id: uuid.UUID) -> Sequence[Column]:
        stmt = select(Column).where(Column.board_id == board_id, Column.deleted_at.is_(None)).order_by(Column.position)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, column_in: ColumnCreate) -> Column:
        db_column = Column(**column_in.model_dump())
        self.session.add(db_column)
        await self.session.commit()
        await self.session.refresh(db_column)
        return db_column

    async def update(self, column_id: uuid.UUID, update_data: dict) -> Column | None:
        stmt = (
            update(Column)
            .where(Column.id == column_id, Column.deleted_at.is_(None))
            .values(**update_data, updated_at=datetime.now(timezone.utc))
            .returning(Column)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one_or_none()

    async def soft_delete(self, column_id: uuid.UUID) -> bool:
        stmt = (
            update(Column)
            .where(Column.id == column_id, Column.deleted_at.is_(None))
            .values(deleted_at=datetime.now(timezone.utc))
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0