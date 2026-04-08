import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class ColumnBase(BaseModel):
    title: str
    position: int

class ColumnCreate(ColumnBase):
    board_id: uuid.UUID

class ColumnResponse(ColumnBase):
    id: uuid.UUID
    board_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)