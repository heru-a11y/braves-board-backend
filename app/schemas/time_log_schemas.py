import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class TimeLogBase(BaseModel):
    start_time: datetime
    stop_time: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    activity_description: Optional[str] = None
    stop_reason: Optional[str] = None

class TimeLogCreate(TimeLogBase):
    task_id: uuid.UUID

class TimeLogResponse(TimeLogBase):
    id: uuid.UUID
    task_id: uuid.UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)