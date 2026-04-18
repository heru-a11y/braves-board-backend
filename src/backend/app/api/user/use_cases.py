from sqlalchemy.ext.asyncio import AsyncSession
from app.api.user.repository import UserRepository
from app.api.user.schema import UserListResponse

class UserUseCase:
    def __init__(self, session: AsyncSession):
        self.user_repo = UserRepository(session)

    async def get_all_users(self):
        users = await self.user_repo.get_all()
        return [UserListResponse.model_validate(user).model_dump(mode='json') for user in users]