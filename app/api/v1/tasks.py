import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.task import TaskCreateRequest, TaskUpdateRequest, TaskMoveRequest
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

@router.get("/{id}", response_model=dict)
async def get_task_detail(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    task_detail = await TaskService.get_task_detail(db, id)
    return {
        "data": task_detail
    }

@router.patch("/{id}", response_model=dict)
async def update_task(
    id: uuid.UUID,
    request: TaskUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    result = await TaskService.update_task(db, id, request)
    return {
        "data": result
    }

@router.patch("/{id}/move", response_model=dict)
async def move_task(
    id: uuid.UUID,
    request: TaskMoveRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    result = await TaskService.move_task(db, id, request)
    return {
        "data": result
    }