import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.task_repository import TaskRepository
from app.repositories.time_log_repository import TimeLogRepository
from app.services.time_tracking_service import TaskTimerService
from app.api.dependencies.auth import get_current_user

router = APIRouter(prefix="/api/v1/tasks", tags=["Task Timer"])

def get_timer_service(db: AsyncSession = Depends(get_db)) -> TaskTimerService:
    task_repo = TaskRepository(db)
    time_log_repo = TimeLogRepository(db)
    return TaskTimerService(task_repo, time_log_repo)

@router.post("/{task_id}/timer/start", status_code=status.HTTP_200_OK)
async def start_timer(
    task_id: uuid.UUID,
    service: TaskTimerService = Depends(get_timer_service),
    current_user=Depends(get_current_user),
):
    return await service.start_timer(task_id)

@router.post("/{task_id}/timer/stop", status_code=status.HTTP_200_OK)
async def stop_timer(
    task_id: uuid.UUID,
    service: TaskTimerService = Depends(get_timer_service),
    current_user=Depends(get_current_user),
):
    return await service.stop_timer(task_id)

@router.post("/{task_id}/timer/ping", status_code=status.HTTP_200_OK)
async def ping_timer(
    task_id: uuid.UUID,
    service: TaskTimerService = Depends(get_timer_service),
    current_user=Depends(get_current_user),
):
    return await service.ping(task_id)

@router.post("/{task_id}/timer/confirm", status_code=status.HTTP_200_OK)
async def confirm_timer(
    task_id: uuid.UUID,
    service: TaskTimerService = Depends(get_timer_service),
    current_user=Depends(get_current_user),
):
    return await service.confirm(task_id)