from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.daily_cleanup_service import CleanupService
from app.repositories.time_log_repository import TimeLogRepository
from app.repositories.task_repository import TaskRepository

router = APIRouter()

@router.post("/tasks/timers/cleanup")
async def system_cleanup(db: AsyncSession = Depends(get_db)):
    task_repo = TaskRepository(db)
    time_log_repo = TimeLogRepository(db)

    service = CleanupService(task_repo, time_log_repo)
    result = await service.run_cleanup()

    return result