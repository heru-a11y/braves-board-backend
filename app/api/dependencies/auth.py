import uuid
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError, ExpiredSignatureError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db, redis_client
from app.repositories.user_repository import UserRepository
from app.exceptions.auth_exceptions import InvalidTokenException, TokenExpiredException
from app.models.user import User

security = HTTPBearer(auto_error=False)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    if not credentials:
        raise InvalidTokenException()

    token = credentials.credentials

    is_blacklisted = await redis_client.get(f"blacklist:{token}")
    if is_blacklisted:
        raise InvalidTokenException()

    try:
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET, 
            algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get("sub")
        token_type = payload.get("type")
        
        if user_id is None or token_type != "access":
            raise InvalidTokenException()
            
        user_id_uuid = uuid.UUID(user_id)
            
    except ExpiredSignatureError:
        raise TokenExpiredException()
    except (JWTError, ValueError):
        raise InvalidTokenException()

    user_repo = UserRepository(db)
    user = await user_repo.get_by_id(user_id_uuid)
    
    if user is None:
        raise InvalidTokenException()
        
    return user