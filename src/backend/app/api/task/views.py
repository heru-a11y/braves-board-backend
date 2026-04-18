import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.connections.postgres import get_db
from app.api.task.schema import TaskCreateRequest, TaskUpdateRequest, TaskMoveRequest, TaskReorderRequest
from app.api.task.use_cases import TaskUseCase
from app.api.depedencies import get_current_user
from app.models.user_model import User
from app.api.standard_response import success_response


router = APIRouter(prefix="/tasks", tags=["Tasks"])


def get_task_use_case(db: AsyncSession = Depends(get_db)) -> TaskUseCase:
    return TaskUseCase(db)


@router.get("", status_code=status.HTTP_200_OK)
async def get_tasks(
    column_id: uuid.UUID,
    use_case: TaskUseCase = Depends(get_task_use_case),
    current_user: User = Depends(get_current_user)
):
    result = await use_case.get_tasks_by_column(column_id)
    return success_response(result)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_task(
    request: TaskCreateRequest,
    use_case: TaskUseCase = Depends(get_task_use_case),
    current_user: User = Depends(get_current_user)
):
    result = await use_case.create_task(request)
    return success_response(result)


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_task_detail(
    id: uuid.UUID,
    use_case: TaskUseCase = Depends(get_task_use_case),
    current_user: User = Depends(get_current_user)
):
    result = await use_case.get_task_detail(id)
    return success_response(result)


@router.patch("/{id}", status_code=status.HTTP_200_OK)
async def update_task(
    id: uuid.UUID,
    request: TaskUpdateRequest,
    use_case: TaskUseCase = Depends(get_task_use_case),
    current_user: User = Depends(get_current_user)
):
    result = await use_case.update_task(id, request)
    return success_response(result)


@router.patch("/{id}/move", status_code=status.HTTP_200_OK)
async def move_task(
    id: uuid.UUID,
    request: TaskMoveRequest,
    use_case: TaskUseCase = Depends(get_task_use_case),
    current_user: User = Depends(get_current_user)
):
    result = await use_case.move_task(id, request)
    return success_response(result)


@router.patch("/{id}/reorder", status_code=status.HTTP_200_OK)
async def reorder_task(
    id: uuid.UUID,
    request: TaskReorderRequest,
    use_case: TaskUseCase = Depends(get_task_use_case),
    current_user: User = Depends(get_current_user)
):
    result = await use_case.reorder_task(id, request)
    return success_response(result)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_task(
    id: uuid.UUID,
    use_case: TaskUseCase = Depends(get_task_use_case),
    current_user: User = Depends(get_current_user)
):
    await use_case.delete_task(id)
    return success_response(None)