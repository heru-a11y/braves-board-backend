from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.connections.postgres import get_db
from app.api.depedencies import get_current_user
from app.models.user_model import User
from app.api.user.use_cases import UserUseCase
from app.api.standard_response import success_response

router = APIRouter(prefix="/users", tags=["Users"])

def get_user_use_case(db: AsyncSession = Depends(get_db)) -> UserUseCase:
    return UserUseCase(db)

@router.get("", status_code=status.HTTP_200_OK)
async def get_all_users(
    use_case: UserUseCase = Depends(get_user_use_case),
    current_user: User = Depends(get_current_user)
):
    result = await use_case.get_all_users()
    return success_response(result)