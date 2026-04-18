import uuid
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr

class UserListResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr
    full_name: str
    picture_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)