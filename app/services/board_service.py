import uuid
from fastapi import HTTPException, status
from app.core.redis import redis_client
from app.schemas.board_schemas import BoardCreate
from app.constants.board_messages import BoardMessage, BoardResponseMessage
from app.repositories.board_repository import BoardRepository
from app.repositories.column_repository import ColumnRepository
from app.repositories.task_repository import TaskRepository
from datetime import datetime, timezone


class BoardService:
    def __init__(self, repo: BoardRepository, session):
        self.repo = repo
        self.column_repo = ColumnRepository(session)
        self.task_repo = TaskRepository(session)

    def _board_to_dict(self, board):
        return {
            "id": str(board.id),
            "title": board.title,
            "user_id": str(board.user_id),
            "created_at": board.created_at,
            "updated_at": board.updated_at,
        }

    async def _lazy_hook(self, user_id: uuid.UUID) -> str:
        key = f"user:{user_id}:last_ping"

        last_ping = await redis_client.get(key)

        if not last_ping:
            return "offline"

        try:
            if isinstance(last_ping, bytes):
                last_ping = last_ping.decode()

            last_ping = datetime.fromisoformat(last_ping)
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
            "data": [self._board_to_dict(b) for b in boards],
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

        columns = await self.column_repo.get_all_by_board_id(board_id)
        columns = columns or []

        tasks = await self.task_repo.get_all_by_board_id(board_id)
        tasks = tasks or []

        tasks_by_column = {}
        for task in tasks:
            col_id = str(task.column_id)
            if col_id not in tasks_by_column:
                tasks_by_column[col_id] = []

            tasks_by_column[col_id].append({
                "id": str(task.id),
                "title": task.title,
                "column_id": str(task.column_id),
                "position": task.position,
                "created_at": task.created_at,
                "updated_at": task.updated_at,
            })

        return {
            "message": BoardResponseMessage.SUCCESS_GET_DETAIL,
            "data": {
                "id": str(board.id),
                "title": board.title,
                "user_id": str(board.user_id),
                "created_at": board.created_at,
                "updated_at": board.updated_at,
                "columns": [
                    {
                        "id": str(c.id),
                        "title": c.title,
                        "board_id": str(c.board_id),
                        "position": c.position,
                        "created_at": c.created_at,
                        "updated_at": c.updated_at,
                        "deleted_at": c.deleted_at,
                        "tasks": tasks_by_column.get(str(c.id), [])  # 🔥 INJECT TASK
                    }
                    for c in columns
                ]
            },
            "meta": {
                "has_columns": len(columns) > 0,
                "status": user_status
            }
        }

    async def create(self, board_in: BoardCreate, user_id: uuid.UUID):
        board = await self.repo.create(board_in, user_id)

        return {
            "message": BoardResponseMessage.SUCCESS_CREATE,
            "data": self._board_to_dict(board)
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
            "data": self._board_to_dict(board)
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