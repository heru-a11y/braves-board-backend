import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, HttpUrl

class TaskAttachmentBase(BaseModel):
    file_name: str
    file_url: str
    type: str

class TaskAttachmentCreate(TaskAttachmentBase):
    task_id: uuid.UUID

class TaskAttachmentResponse(TaskAttachmentBase):
    id: uuid.UUID
    task_id: uuid.UUID
    uploaded_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AddLinkRequest(BaseModel):
    title: Optional[str] = None
    url: HttpUrl