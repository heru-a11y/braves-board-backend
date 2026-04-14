import uuid
from pydantic import BaseModel, EmailStr
from datetime import datetime

class AuthUrlData(BaseModel):
    auth_url: str

class AuthUrlResponse(BaseModel):
    data: AuthUrlData

class AuthCallbackRequest(BaseModel):
    code: str

class TokenData(BaseModel):
    id: uuid.UUID
    email: EmailStr
    google_id: str
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class TokenResponse(BaseModel):
    data: TokenData

class CurrentUserData(BaseModel):
    id: uuid.UUID
    email: EmailStr
    google_id: str
    full_name: str          
    picture_url: str | None
    created_at: datetime

class CurrentUserResponse(BaseModel):
    data: CurrentUserData

class AccessTokenData(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class AccessTokenResponse(BaseModel):
    data: AccessTokenData

class LogoutData(BaseModel):
    message: str

class LogoutResponse(BaseModel):
    data: LogoutData