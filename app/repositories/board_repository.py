import uuid
from datetime import datetime, timezone
from typing import Sequence
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.board import Board
from app.schemas.board import BoardCreate

class BoardRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, board_id: uuid.UUID) -> Board | None:
        stmt = select(Board).where(Board.id == board_id, Board.deleted_at.is_(None))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all_by_user_id(self, user_id: uuid.UUID) -> Sequence[Board]:
        stmt = select(Board).where(Board.user_id == user_id, Board.deleted_at.is_(None))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, board_in: BoardCreate) -> Board:
        db_board = Board(**board_in.model_dump())
        self.session.add(db_board)
        await self.session.commit()
        await self.session.refresh(db_board)
        return db_board

    async def update(self, board_id: uuid.UUID, update_data: dict) -> Board | None:
        stmt = (
            update(Board)
            .where(Board.id == board_id, Board.deleted_at.is_(None))
            .values(**update_data, updated_at=datetime.now(timezone.utc))
            .returning(Board)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one_or_none()

    async def soft_delete(self, board_id: uuid.UUID) -> bool:
        stmt = (
            update(Board)
            .where(Board.id == board_id, Board.deleted_at.is_(None))
            .values(deleted_at=datetime.now(timezone.utc))
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0