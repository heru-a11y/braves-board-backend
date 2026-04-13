import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.dependencies.auth import get_current_user
from app.models.user import User
from app.services.subtask_service import SubtaskService
from app.schemas.subtask import SubtaskCreateRequest, SubtaskUpdateRequest, SubtaskMoveRequest
from app.constants import subtask_messages

router = APIRouter(prefix="/api/v1", tags=["Subtasks"])

@router.post(
    "/tasks/{task_id}/subtasks",
    status_code=status.HTTP_201_CREATED,
    response_model=dict
)
async def create_subtask(
    task_id: uuid.UUID,
    payload: SubtaskCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = SubtaskService(db)
    subtask = await service.create_subtask(task_id, payload)
    return {"data": subtask}

@router.patch(
    "/subtasks/{subtask_id}",
    status_code=status.HTTP_200_OK,
    response_model=dict
)
async def update_subtask(
    subtask_id: uuid.UUID,
    payload: SubtaskUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = SubtaskService(db)
    subtask = await service.update_subtask(subtask_id, payload)
    return {"data": subtask}

@router.patch(
    "/subtasks/{subtask_id}/move",
    status_code=status.HTTP_200_OK,
    response_model=dict
)
async def move_subtask(
    subtask_id: uuid.UUID,
    payload: SubtaskMoveRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = SubtaskService(db)
    subtask = await service.move_subtask(subtask_id, payload)
    return {"data": subtask}

@router.delete(
    "/subtasks/{subtask_id}",
    status_code=status.HTTP_200_OK,
    response_model=dict
)
async def delete_subtask(
    subtask_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = SubtaskService(db)
    await service.delete_subtask(subtask_id)
    return {"data": {"message": subtask_messages.SUBTASK_DELETED_SUCCESS}}