import uuid
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.board_repository import BoardRepository
from app.services.board_service import BoardService
from app.schemas.board_schemas import BoardCreate, BoardUpdate
from app.api.dependencies.auth import get_current_user

router = APIRouter(prefix="/api/v1/boards", tags=["Boards"])

def get_board_service(db: AsyncSession = Depends(get_db)) -> BoardService:
    repo = BoardRepository(db)
    return BoardService(repo)

@router.get("", status_code=status.HTTP_200_OK)
async def get_boards(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: BoardService = Depends(get_board_service),
    current_user=Depends(get_current_user),
):
    return await service.get_all(current_user.id, limit, offset)

@router.get("/{board_id}", status_code=status.HTTP_200_OK)
async def get_board_detail(
    board_id: uuid.UUID,
    service: BoardService = Depends(get_board_service),
    current_user=Depends(get_current_user),
):
    return await service.get_detail(board_id, current_user.id)

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_board(
    board_in: BoardCreate,
    service: BoardService = Depends(get_board_service),
    current_user=Depends(get_current_user),
):
    return await service.create(board_in, current_user.id)

@router.patch("/{board_id}", status_code=status.HTTP_200_OK)
async def update_board(
    board_id: uuid.UUID,
    update_data: BoardUpdate,
    service: BoardService = Depends(get_board_service),
    current_user=Depends(get_current_user),
):
    return await service.update(
        board_id,
        update_data.model_dump(exclude_unset=True),
        current_user.id,
    )

@router.delete("/{board_id}", status_code=status.HTTP_200_OK)
async def delete_board(
    board_id: uuid.UUID,
    service: BoardService = Depends(get_board_service),
    current_user=Depends(get_current_user),
):
    return await service.delete(board_id, current_user.id)