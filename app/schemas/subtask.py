import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class SubtaskBase(BaseModel):
    title: str
    is_completed: bool = False
    position: int

class SubtaskCreateRequest(BaseModel):
    title: str

class SubtaskCreate(SubtaskBase):
    task_id: uuid.UUID

class SubtaskUpdateRequest(BaseModel):
    title: Optional[str] = None
    is_completed: Optional[bool] = None

class SubtaskResponse(SubtaskBase):
    id: uuid.UUID
    task_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class SubtaskSimpleResponse(BaseModel):
    id: uuid.UUID
    title: str
    is_completed: bool
    position: int

    model_config = ConfigDict(from_attributes=True)

class SubtaskUpdateResponse(BaseModel):
    id: uuid.UUID
    title: str
    is_completed: bool
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)