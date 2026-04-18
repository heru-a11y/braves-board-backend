import uuid
from typing import Sequence, List
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user_model import User

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> Sequence[User]:
        stmt = select(User).where(User.deleted_at.is_(None)).order_by(User.full_name)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def check_users_exist(self, user_ids: List[uuid.UUID]) -> bool:
        unique_ids = list(set(user_ids))
        stmt = select(func.count(User.id)).where(User.id.in_(unique_ids), User.deleted_at.is_(None))
        result = await self.session.execute(stmt)
        count = result.scalar()
        return count == len(unique_ids)