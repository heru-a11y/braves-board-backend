import uuid
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.task_comment_service import TaskCommentService
from app.api.dependencies.auth import get_current_user

router = APIRouter(prefix="/api/v1/tasks", tags=["Task Comments"])


class AddCommentRequest(BaseModel):
    content: str


@router.post(
    "/{id}/comments",
    status_code=status.HTTP_201_CREATED,
    response_model=dict,
)
async def add_comment(
    id: uuid.UUID,
    request: AddCommentRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await TaskCommentService.add_comment(
        db=db,
        task_id=id,
        content=request.content,
        current_user_id=current_user.id,
    )
    return {"data": result}


@router.delete(
    "/{id}/comments/{comment_id}",
    response_model=dict,
)
async def delete_comment(
    id: uuid.UUID,
    comment_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await TaskCommentService.delete_comment(
        db=db,
        task_id=id,
        comment_id=comment_id,
        current_user_id=current_user.id,
    )
    return {"data": result}