# type: ignore
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, Response, Cookie
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt

from app.core.config import settings
from app.core.database import get_db, redis_client
from app.repositories.user_repository import UserRepository
from app.schemas.auth import (
    AuthUrlResponse, 
    AuthCallbackRequest, 
    TokenResponse, 
    CurrentUserResponse,
    AccessTokenResponse,
    LogoutResponse
)
from app.services.auth_service import AuthService
from app.api.dependencies.auth import get_current_user, security
from app.models.user import User
from app.exceptions.auth_exceptions import InvalidRefreshTokenException
from app.constants import auth_messages

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])

@router.get("/google/login", response_model=AuthUrlResponse)
async def google_login():
    auth_url = AuthService.get_google_auth_url()
    return {"data": {"auth_url": auth_url}}

@router.post("/google/callback", response_model=TokenResponse)
async def google_callback(
    request: AuthCallbackRequest, 
    response: Response, 
    db: AsyncSession = Depends(get_db)
):
    user_repo = UserRepository(db)
    result = await AuthService.handle_google_callback(request.code, user_repo)
    
    response.set_cookie(
        key="refresh_token",
        value=result["refresh_token"],
        httponly=True,
        secure=True, 
        samesite="lax",
        path="/"
    )
    
    return {
        "data": {
            "id": result["user"].id,
            "email": result["user"].email,
            "google_id": result["user"].google_id,
            "access_token": result["access_token"],
            "token_type": "bearer",
            "expires_in": result["expires_in"]
        }
    }

@router.get("/me", response_model=CurrentUserResponse)
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    return {
        "data": {
            "id": current_user.id,
            "email": current_user.email,
            "google_id": current_user.google_id,
            "full_name": current_user.full_name,
            "picture_url": current_user.picture_url,
            "created_at": current_user.created_at
        }
    }

@router.post("/refresh", response_model=AccessTokenResponse)
async def refresh_token(
    refresh_token: str | None = Cookie(default=None),
    db: AsyncSession = Depends(get_db)
):
    if not refresh_token:
        raise InvalidRefreshTokenException()

    user_repo = UserRepository(db)
    result = await AuthService.refresh_access_token(refresh_token, user_repo)

    return {
        "data": {
            "access_token": result["access_token"],
            "token_type": "bearer",
            "expires_in": result["expires_in"]
        }
    }

@router.post("/logout", response_model=LogoutResponse)
async def logout(
    response: Response,
    current_user: User = Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    payload = jwt.decode(
        token, 
        settings.JWT_SECRET, 
        algorithms=[settings.ALGORITHM], 
        options={"verify_exp": False}
    )
    
    exp_timestamp = payload.get("exp")
    now_timestamp = int(datetime.now(timezone.utc).timestamp())
    
    ttl = exp_timestamp - now_timestamp

    if ttl > 0:
        await redis_client.setex(f"blacklist:{token}", ttl, "true")

    response.delete_cookie(
        key="refresh_token",
        path="/",
        secure=True,
        httponly=True,
        samesite="lax"
    )
    
    return {
        "data": {
            "message": auth_messages.LOGOUT_SUCCESS
        }
    }