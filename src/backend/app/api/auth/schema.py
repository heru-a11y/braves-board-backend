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

class AuthUrlData(BaseModel):
    auth_url: str

class AuthCallbackRequest(BaseModel):
    code: str

class TokenData(BaseModel):
    id: uuid.UUID
    email: EmailStr
    google_id: Optional[str] = None
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class CurrentUserData(BaseModel):
    id: uuid.UUID
    email: EmailStr
    full_name: str
    picture_url: Optional[str] = None
    created_at: datetime

class AccessTokenData(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class LogoutData(BaseModel):
    message: str