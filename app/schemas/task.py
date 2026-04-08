import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    labels: Optional[List[str]] = None
    position: int
    is_timer_running: bool = False
    assignee_ids: Optional[List[uuid.UUID]] = None

class TaskCreate(TaskBase):
    column_id: uuid.UUID

class TaskResponse(TaskBase):
    id: uuid.UUID
    column_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)