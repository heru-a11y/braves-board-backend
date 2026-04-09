import httpx
import urllib.parse
from fastapi import status
from app.core.config import settings
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.utils import jwt_utils
from app.exceptions.auth_exceptions import (
    GoogleAuthException, 
    InvalidGoogleCodeException, 
    ForbiddenDomainException
)

class AuthService:
    @staticmethod
    def get_google_auth_url() -> str:
        try:
            base_url = "https://accounts.google.com/o/oauth2/v2/auth"
            params = {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                "response_type": "code",
                "scope": "openid email profile",
                "access_type": "offline",
                "prompt": "consent"
            }
            return f"{base_url}?{urllib.parse.urlencode(params)}"
        except Exception:
            raise GoogleAuthException()
        
    @staticmethod
    async def handle_google_callback(code: str, user_repo: UserRepository):
        # Memastikan karakter seperti %2F diubah kembali menjadi /
        decoded_code = urllib.parse.unquote(code)

        async with httpx.AsyncClient() as client:
            token_url = "https://oauth2.googleapis.com/token"
            data = {
                "code": decoded_code,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            }
            res = await client.post(token_url, data=data)
            
            if res.status_code != 200:
                raise InvalidGoogleCodeException()
            
            google_tokens = res.json()
            access_token = google_tokens.get("access_token")

            user_info_res = await client.get(
                "https://www.googleapis.com/oauth2/v3/userinfo",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            profile = user_info_res.json()
            email = profile.get("email")

            if not email or not email.endswith("@bangunindo.com"):
                raise ForbiddenDomainException()

            user = await user_repo.get_by_google_id(profile.get("sub"))
            if not user:
                user_in = UserCreate(
                    email=email,
                    full_name=profile.get("name"),
                    picture_url=profile.get("picture"),
                    google_id=profile.get("sub")
                )
                user = await user_repo.create(user_in)
            
            token_payload = {"sub": str(user.id)}
            access_token = jwt_utils.create_access_token(token_payload)
            refresh_token = jwt_utils.create_refresh_token(token_payload)

            return {
                "user": user,
                "access_token": access_token,
                "refresh_token": refresh_token,
                "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
            }
        # 1. Tukar Code dengan Token Google
        async with httpx.AsyncClient() as client:
            token_url = "https://oauth2.googleapis.com/token"
            data = {
                "code": code,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            }
            res = await client.post(token_url, data=data)
            if res.status_code != 200:
                raise InvalidGoogleCodeException()
            
            google_tokens = res.json()
            access_token = google_tokens.get("access_token")

            # 2. Ambil Profil User dari Google
            user_info_res = await client.get(
                "https://www.googleapis.com/oauth2/v3/userinfo",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            profile = user_info_res.json()
            email = profile.get("email")

            # 3. Validasi Domain @bangunindo.com [cite: 736]
            if not email or not email.endswith("@bangunindo.com"):
                raise ForbiddenDomainException()

            # 4. Upsert User ke Database [cite: 739]
            user = await user_repo.get_by_google_id(profile.get("sub"))
            if not user:
                user_in = UserCreate(
                    email=email,
                    full_name=profile.get("name"),
                    picture_url=profile.get("picture"),
                    google_id=profile.get("sub")
                )
                user = await user_repo.create(user_in)
            
            # 5. Generate Internal Tokens 
            token_payload = {"sub": str(user.id)}
            access_token = jwt_utils.create_access_token(token_payload)
            refresh_token = jwt_utils.create_refresh_token(token_payload)

            return {
                "user": user,
                "access_token": access_token,
                "refresh_token": refresh_token,
                "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
            }