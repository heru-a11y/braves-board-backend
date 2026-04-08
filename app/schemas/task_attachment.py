import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class TaskAttachmentBase(BaseModel):
    file_name: str
    file_url: str

class TaskAttachmentCreate(TaskAttachmentBase):
    task_id: uuid.UUID

class TaskAttachmentResponse(TaskAttachmentBase):
    id: uuid.UUID
    task_id: uuid.UUID
    uploaded_at: datetime

    model_config = ConfigDict(from_attributes=True)