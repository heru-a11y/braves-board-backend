import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, field_validator


class BoardBase(BaseModel):
    title: str

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str):
        if not v or not v.strip():
            raise ValueError("Title tidak boleh kosong")
        if len(v) > 255:
            raise ValueError("Title maksimal 255 karakter")
        return v.strip()


class BoardCreate(BoardBase):
    pass


class BoardUpdate(BaseModel):
    title: Optional[str] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, v):
        if v is None:
            return v
        if not v.strip():
            raise ValueError("Title tidak boleh kosong")
        if len(v) > 255:
            raise ValueError("Title maksimal 255 karakter")
        return v.strip()


class BoardResponse(BoardBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    columns: list = []

    model_config = ConfigDict(from_attributes=True)