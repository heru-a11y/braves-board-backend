import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.subtask_repository import SubtaskRepository
from app.repositories.task_repository import TaskRepository
from app.schemas.subtask import (
    SubtaskCreateRequest,
    SubtaskCreate,
    SubtaskSimpleResponse,
    SubtaskUpdateRequest,
    SubtaskUpdateResponse,
)
from app.exceptions.task_exceptions import TaskNotFoundException
from app.exceptions.subtask_exceptions import (
    SubtaskNotFoundException,
    NoSubtaskFieldsToUpdateException,
)

class SubtaskService:
    def __init__(self, db: AsyncSession):
        self.subtask_repo = SubtaskRepository(db)
        self.task_repo = TaskRepository(db)

    async def create_subtask(
        self,
        task_id: uuid.UUID,
        payload: SubtaskCreateRequest
    ) -> SubtaskSimpleResponse:
        task = await self.task_repo.get_by_id(task_id)
        if not task:
            raise TaskNotFoundException()

        max_position = await self.subtask_repo.get_max_position(task_id)
        next_position = max_position + 1

        subtask_in = SubtaskCreate(
            task_id=task_id,
            title=payload.title,
            position=next_position
        )
        subtask = await self.subtask_repo.create(subtask_in)

        return SubtaskSimpleResponse.model_validate(subtask)

    async def update_subtask(
        self,
        subtask_id: uuid.UUID,
        payload: SubtaskUpdateRequest
    ) -> SubtaskUpdateResponse:
        update_data = payload.model_dump(exclude_unset=True)
        if not update_data:
            raise NoSubtaskFieldsToUpdateException()

        subtask = await self.subtask_repo.get_by_id(subtask_id)
        if not subtask:
            raise SubtaskNotFoundException()

        updated_subtask = await self.subtask_repo.update(subtask_id, update_data)

        return SubtaskUpdateResponse.model_validate(updated_subtask)