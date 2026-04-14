import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.column import ColumnCreate, ColumnUpdate
from app.schemas.column_response import ColumnSingleResponse, ColumnListResponse
from app.services.column_service import ColumnService
from app.api.dependencies.auth import get_current_user

router = APIRouter(prefix="/api/v1/boards/{board_id}/columns", tags=["Columns"])


def get_column_service(db: AsyncSession = Depends(get_db)) -> ColumnService:
    return ColumnService(db)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ColumnSingleResponse)
async def create_column(
    board_id: uuid.UUID,
    payload: ColumnCreate,
    service: ColumnService = Depends(get_column_service),
    _=Depends(get_current_user),
):
    payload.board_id = board_id
    return await service.create_column(payload)


@router.get("/{column_id}", status_code=status.HTTP_200_OK, response_model=ColumnSingleResponse)
async def get_column(
    column_id: uuid.UUID,
    service: ColumnService = Depends(get_column_service),
    _=Depends(get_current_user),
):
    return await service.get_by_id(column_id)


@router.get("", status_code=status.HTTP_200_OK, response_model=ColumnListResponse)
async def get_columns(
    board_id: uuid.UUID,
    service: ColumnService = Depends(get_column_service),
    _=Depends(get_current_user),
):
    return await service.get_all_by_board_id(board_id)


@router.patch("/{column_id}", status_code=status.HTTP_200_OK, response_model=ColumnSingleResponse)
async def update_column(
    column_id: uuid.UUID,
    payload: ColumnUpdate,
    service: ColumnService = Depends(get_column_service),
    _=Depends(get_current_user),
):
    return await service.update_column(
        column_id,
        payload.model_dump(exclude_unset=True),
    )


@router.delete("/{column_id}", status_code=status.HTTP_200_OK)
async def delete_column(
    column_id: uuid.UUID,
    service: ColumnService = Depends(get_column_service),
    _=Depends(get_current_user),
):
    return await service.delete_column(column_id)


@router.patch("/{column_id}/reorder", status_code=status.HTTP_200_OK, response_model=ColumnSingleResponse)
async def reorder_column(
    column_id: uuid.UUID,
    new_position: int,
    service: ColumnService = Depends(get_column_service),
    _=Depends(get_current_user),
):
    return await service.reorder_column(column_id, new_position)