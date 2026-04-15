import uuid
from fastapi import HTTPException, status
from app.core.redis import redis_client
from app.schemas.board_schemas import BoardCreate
from app.constants.board_messages import BoardMessage, BoardResponseMessage
from app.repositories.board_repository import BoardRepository
from datetime import datetime, timezone

class BoardService:
    def __init__(self, repo: BoardRepository):
        self.repo = repo

    async def _lazy_hook(self, user_id: uuid.UUID) -> str:
        key = f"user:{user_id}:last_ping"

        last_ping = await redis_client.get(key)

        if not last_ping:
            return "offline"

        try:
            last_ping = datetime.fromisoformat(last_ping.decode())
        except Exception:
            return "offline"

        if last_ping.tzinfo is None:
            last_ping = last_ping.replace(tzinfo=timezone.utc)

        now = datetime.now(timezone.utc)
        diff = (now - last_ping).total_seconds()

        if diff > 3 * 3600:
            return "offline"
        elif diff > 5 * 60:
            return "idle"

        return "online"

    async def get_all(
        self,
        user_id: uuid.UUID,
        limit: int = 10,
        offset: int = 0
    ):
        user_status = await self._lazy_hook(user_id)

        boards = await self.repo.get_all(user_id, limit, offset)

        return {
            "message": BoardResponseMessage.SUCCESS_GET_ALL,
            "data": boards,
            "meta": {
                "limit": limit,
                "offset": offset,
                "count": len(boards),
                "status": user_status
            }
        }

    async def get_detail(self, board_id: uuid.UUID, user_id: uuid.UUID):
        user_status = await self._lazy_hook(user_id)

        board = await self.repo.get_by_id(board_id, user_id)
        if not board:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=BoardMessage.NOT_FOUND
            )

        return {
            "message": BoardResponseMessage.SUCCESS_GET_DETAIL,
            "data": board,
            "meta": {
                "has_columns": True,
                "status": user_status
            }
        }

    async def create(self, board_in: BoardCreate, user_id: uuid.UUID):
        board = await self.repo.create(board_in, user_id)

        return {
            "message": BoardResponseMessage.SUCCESS_CREATE,
            "data": board
        }

    async def update(
        self,
        board_id: uuid.UUID,
        update_data: dict,
        user_id: uuid.UUID
    ):
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=BoardMessage.INVALID_UPDATE
            )

        board = await self.repo.update(board_id, update_data, user_id)
        if not board:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=BoardMessage.NOT_FOUND
            )

        return {
            "message": BoardResponseMessage.SUCCESS_UPDATE,
            "data": board
        }

    async def delete(self, board_id: uuid.UUID, user_id: uuid.UUID):
        success = await self.repo.soft_delete(board_id, user_id)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=BoardMessage.NOT_FOUND
            )

        return {
            "message": BoardResponseMessage.SUCCESS_DELETE
        }