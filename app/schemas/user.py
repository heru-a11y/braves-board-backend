import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    picture_url: Optional[str] = None

class UserCreate(UserBase):
    google_id: Optional[str] = None

class UserResponse(UserBase):
    id: uuid.UUID
    google_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)