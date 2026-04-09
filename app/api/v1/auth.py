from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.auth import AuthUrlResponse, AuthCallbackRequest, TokenResponse
from app.services.auth_service import AuthService

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
    
    # Set Refresh Token di Cookie (Secure & HttpOnly) [cite: 746, 82]
    response.set_cookie(
        key="refresh_token",
        value=result["refresh_token"],
        httponly=True,
        secure=True,  # Set True untuk produksi (HTTPS)
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