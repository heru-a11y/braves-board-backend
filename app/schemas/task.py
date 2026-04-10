import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict

from app.schemas.subtask import SubtaskResponse
from app.schemas.task_comment import TaskCommentResponse
from app.schemas.task_attachment import TaskAttachmentResponse

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
    due_date: Optional[datetime] = None
    labels: Optional[List[str]] = None
    assignee_ids: Optional[List[uuid.UUID]] = None
    comment_count: int
    attachment_count: int
    is_timer_running: bool

class TaskDetailResponse(TaskBase):
    id: uuid.UUID
    subtasks: List[SubtaskResponse] = []
    comments: List[TaskCommentResponse] = []
    attachments: List[TaskAttachmentResponse] = []

    model_config = ConfigDict(from_attributes=True)

class TaskUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    labels: Optional[List[str]] = None
    assignee_ids: Optional[List[uuid.UUID]] = None

class TaskMoveRequest(BaseModel):
    column_id: uuid.UUID