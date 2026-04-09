import uuid
from pydantic import BaseModel, EmailStr

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