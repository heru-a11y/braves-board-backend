import uuid
from typing import Any, Optional

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.task_repository import TaskRepository
from app.repositories.time_log_repository import TimeLogRepository
from app.services.time_tracking_service import TaskTimerService
from app.schemas.time_log_schemas import TimeLogsResponse
from app.api.dependencies.auth import get_current_user

router = APIRouter(prefix="/api/v1/tasks", tags=["Task Timer"])

class TimerPayload(BaseModel):
    description: Optional[str] = None


class TimerResponse(BaseModel):
    message: str
    data: Any | None = None

def get_timer_service(db: AsyncSession = Depends(get_db)) -> TaskTimerService:
    task_repo = TaskRepository(db)
    time_log_repo = TimeLogRepository(db)
    return TaskTimerService(task_repo, time_log_repo)

@router.post(
    "/{task_id}/timer/start",
    status_code=status.HTTP_200_OK,
    response_model=TimerResponse
)
async def start_timer(
    task_id: uuid.UUID,
    payload: TimerPayload | None = None,
    service: TaskTimerService = Depends(get_timer_service),
    current_user=Depends(get_current_user),
):
    description = payload.description if payload else None
    return await service.start_timer(task_id, description)


@router.post(
    "/{task_id}/timer/stop",
    status_code=status.HTTP_200_OK,
    response_model=TimerResponse
)
async def stop_timer(
    task_id: uuid.UUID,
    service: TaskTimerService = Depends(get_timer_service),
    current_user=Depends(get_current_user),
):
    return await service.stop_timer(task_id)


@router.post(
    "/{task_id}/timer/ping",
    status_code=status.HTTP_200_OK,
    response_model=TimerResponse
)
async def ping_timer(
    task_id: uuid.UUID,
    service: TaskTimerService = Depends(get_timer_service),
    current_user=Depends(get_current_user),
):
    return await service.ping(task_id)


@router.post(
    "/{task_id}/timer/confirm",
    status_code=status.HTTP_200_OK,
    response_model=TimerResponse
)
async def confirm_timer(
    task_id: uuid.UUID,
    service: TaskTimerService = Depends(get_timer_service),
    current_user=Depends(get_current_user),
):
    return await service.confirm(task_id)


@router.get(
    "/{task_id}/timer/logs",
    status_code=status.HTTP_200_OK,
    response_model=TimeLogsResponse
)
async def get_time_logs(
    task_id: uuid.UUID,
    service: TaskTimerService = Depends(get_timer_service),
    current_user=Depends(get_current_user),
):
    return await service.get_time_logs(task_id)