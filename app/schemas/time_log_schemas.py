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


class TimeLogCreate(BaseModel):
    task_id: uuid.UUID
    start_time: datetime
    activity_description: Optional[str] = None

class TimeLogResponse(TimeLogBase):
    id: uuid.UUID
    start_time: datetime
    stop_time: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    activity_description: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class TimeLogItem(BaseModel):
    id: uuid.UUID
    start_time: datetime
    stop_time: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    activity_description: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TimeLogsResponse(BaseModel):
    task_id: uuid.UUID
    count: int
    logs: list[TimeLogItem]