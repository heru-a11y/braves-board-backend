import uuid
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.column import ColumnCreate
from app.constants.column_messages import SuccessMessage, ErrorMessage
from app.repositories.column_repository import ColumnRepository


class ColumnService:
    def __init__(self, session: AsyncSession):
        self.repo = ColumnRepository(session)

    async def get_by_id(self, column_id: uuid.UUID):
        column = await self.repo.get_by_id(column_id)

        if not column:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ErrorMessage.COLUMN_NOT_FOUND
            )

        return {
            "message": SuccessMessage.COLUMN_FETCHED,
            "data": column
        }

    async def get_all_by_board_id(self, board_id: uuid.UUID):
        columns = await self.repo.get_all_by_board_id(board_id)

        return {
            "message": SuccessMessage.COLUMNS_FETCHED,
            "data": columns
        }

    async def create_column(self, column_in: ColumnCreate):
        column = await self.repo.create(column_in)

        return {
            "message": SuccessMessage.COLUMN_CREATED,
            "data": column
        }

    async def update_column(self, column_id: uuid.UUID, update_data: dict):
        column = await self.repo.update(column_id, update_data)

        if not column:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ErrorMessage.COLUMN_NOT_FOUND
            )

        return {
            "message": SuccessMessage.COLUMN_UPDATED,
            "data": column
        }

    async def delete_column(self, column_id: uuid.UUID):
        success = await self.repo.soft_delete(column_id)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ErrorMessage.COLUMN_NOT_FOUND
            )

        return {
            "message": SuccessMessage.COLUMN_DELETED
        }

    async def reorder_column(self, column_id: uuid.UUID, new_position: int):
        column = await self.repo.reorder(column_id, new_position)

        if not column:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorMessage.INVALID_POSITION
            )

        return {
            "message": SuccessMessage.COLUMN_REORDERED,
            "data": column
        }