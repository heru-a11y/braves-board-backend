# type: ignore
import uuid
from fastapi import UploadFile
from app.schemas.task_attachment_schemas import TaskAttachmentCreate
from app.repositories.task_attachment_repository import TaskAttachmentRepository
from app.utils.storage_util import StorageUtil
from app.exceptions.task_attachment_exceptions import (
    InvalidFileTypeException,
    ImageTooLargeException,
    PDFTooLargeException,
    VideoTooLargeException
)

ALLOWED_MIME_TYPES = {
    "image/jpeg": ("image", 10 * 1024 * 1024),
    "image/png": ("image", 10 * 1024 * 1024),
    "image/webp": ("image", 10 * 1024 * 1024),
    "application/pdf": ("pdf", 50 * 1024 * 1024),
    "video/mp4": ("video", 1000 * 1024 * 1024)
}

class TaskAttachmentService:
    def __init__(self, repository: TaskAttachmentRepository):
        self.repository = repository
        self.storage_util = StorageUtil()

    async def upload_file(self, task_id: uuid.UUID, file: UploadFile):
        file_info = ALLOWED_MIME_TYPES.get(file.content_type)
        if not file_info:
            raise InvalidFileTypeException()

        file_type, max_size = file_info

        file.file.seek(0, 2)
        file_size = file.file.tell()
        file.file.seek(0)

        if file_size > max_size:
            if file_type == "image":
                raise ImageTooLargeException()
            elif file_type == "pdf":
                raise PDFTooLargeException()
            elif file_type == "video":
                raise VideoTooLargeException()

        file_extension = file.filename.split(".")[-1]
        destination_path = f"tasks/{task_id}/{uuid.uuid4()}.{file_extension}"
        
        file_url = self.storage_util.upload_file(file, destination_path)

        attachment_in = TaskAttachmentCreate(
            task_id=task_id,
            type=file_type,
            file_name=file.filename,
            file_url=file_url
        )

        return await self.repository.create(attachment_in)

    def generate_signed_url(self, file_url: str) -> str:
        return self.storage_util.generate_signed_url(file_url)

    async def add_link(self, task_id: uuid.UUID, title: str | None, url: str):
        attachment_in = TaskAttachmentCreate(
            task_id=task_id,
            type="link",
            file_name=title if title and title.strip() else url,
            file_url=url,
        )
        return await self.repository.create(attachment_in)