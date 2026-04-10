import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.task import TaskCreateRequest
from app.services.task_service import TaskService
from app.api.dependencies.auth import get_current_user

router = APIRouter(prefix="/api/v1/tasks", tags=["Tasks"])

@router.get("", response_model=dict)
async def get_tasks(
    column_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    tasks = await TaskService.get_tasks_by_column(db, column_id)
    return {
        "data": tasks
    }

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_task(
    request: TaskCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    task = await TaskService.create_task(db, request)
    return {
        "data": {
            "id": task.id,
            "title": task.title
        }
    }