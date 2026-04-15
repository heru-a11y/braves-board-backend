import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class ColumnBase(BaseModel):
    title: str


class ColumnCreate(ColumnBase):
    board_id: uuid.UUID


class ColumnUpdate(BaseModel):
    title: Optional[str] = None
    position: Optional[int] = None


class ColumnResponse(ColumnBase):
    id: uuid.UUID
    board_id: uuid.UUID
    position: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class ColumnSingleResponse(BaseModel):
    message: str
    data: ColumnResponse


class ColumnListResponse(BaseModel):
    message: str
    data: List[ColumnResponse]