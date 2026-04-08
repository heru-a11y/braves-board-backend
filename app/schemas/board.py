import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class BoardBase(BaseModel):
    title: str

class BoardCreate(BoardBase):
    user_id: uuid.UUID

class BoardResponse(BoardBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)