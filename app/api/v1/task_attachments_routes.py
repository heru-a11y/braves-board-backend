import uuid
from fastapi import APIRouter, Depends, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.dependencies.auth import get_current_user
from app.schemas.task_attachment_schemas import TaskAttachmentResponse, AddLinkRequest
from app.repositories.task_attachment_repository import TaskAttachmentRepository
from app.services.task_attachment_service import TaskAttachmentService

router = APIRouter(prefix="/tasks/{task_id}/attachments", tags=["Task Attachments"])

@router.post("/file", response_model=dict, status_code=status.HTTP_201_CREATED)
async def upload_task_attachment(
    task_id: uuid.UUID,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    repository = TaskAttachmentRepository(db)
    service = TaskAttachmentService(repository)
    attachment = await service.upload_file(task_id, file)
    
    attachment_dict = TaskAttachmentResponse.model_validate(attachment).model_dump(mode="json")
    attachment_dict["file_url"] = service.generate_signed_url(attachment.file_url)
    
    return {
        "data": attachment_dict
    }


@router.post("/link", response_model=dict, status_code=status.HTTP_201_CREATED)
async def add_task_attachment_link(
    task_id: uuid.UUID,
    request: AddLinkRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    repository = TaskAttachmentRepository(db)
    service = TaskAttachmentService(repository)
    attachment = await service.add_link(
        task_id=task_id,
        title=request.title,
        url=str(request.url),
    )

    attachment_dict = TaskAttachmentResponse.model_validate(attachment).model_dump(mode="json")

    return {"data": attachment_dict}