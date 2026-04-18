import uuid
from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel, ConfigDict, model_validator


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
    start_time: Optional[datetime] = None
    total_duration: Optional[int] = 0

    model_config = ConfigDict(from_attributes=True)


class TaskCreateRequest(BaseModel):
    column_id: uuid.UUID
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    labels: Optional[List[str]] = None
    assignee_ids: Optional[List[uuid.UUID]] = None


class TaskListResponse(BaseModel):
    id: uuid.UUID
    title: str
    position: int
    due_date: Optional[datetime] = None
    labels: Optional[List[str]] = None
    assignee_ids: Optional[List[uuid.UUID]] = None
    comment_count: int
    attachment_count: int
    is_timer_running: bool
    total_duration: Optional[int] = 0


class SubtaskNestedResponse(BaseModel):
    id: uuid.UUID
    title: str
    is_completed: bool
    position: int
    
    model_config = ConfigDict(from_attributes=True)


class CommentNestedResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    user_name: str
    content: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode='before')
    @classmethod
    def map_user_name(cls, data: Any) -> Any:
        if hasattr(data, 'user') and data.user:
            setattr(data, 'user_name', data.user.full_name)
        return data

class AttachmentNestedResponse(BaseModel):
    id: uuid.UUID
    type: str
    file_name: str
    file_url: str
    uploaded_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class TaskDetailResponse(TaskBase):
    id: uuid.UUID
    subtasks: List[SubtaskNestedResponse] = []
    comments: List[CommentNestedResponse] = []
    attachments: List[AttachmentNestedResponse] = []

    model_config = ConfigDict(from_attributes=True)


class TaskUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    labels: Optional[List[str]] = None
    assignee_ids: Optional[List[uuid.UUID]] = None


class TaskMoveRequest(BaseModel):
    column_id: uuid.UUID
    position: int


class TaskMoveResponse(BaseModel):
    id: uuid.UUID
    column_id: uuid.UUID
    position: int

    model_config = ConfigDict(from_attributes=True)


class TaskReorderRequest(BaseModel):
    position: int


class TaskReorderResponse(BaseModel):
    id: uuid.UUID
    position: int
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)