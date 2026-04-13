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
    SubtaskMoveRequest,
    SubtaskMoveResponse,
)
from app.exceptions.task_exceptions import TaskNotFoundException
from app.exceptions.subtask_exceptions import (
    SubtaskNotFoundException,
    NoSubtaskFieldsToUpdateException,
    InvalidSubtaskPositionException,
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

    async def move_subtask(
        self,
        subtask_id: uuid.UUID,
        payload: SubtaskMoveRequest
    ) -> SubtaskMoveResponse:
        subtask = await self.subtask_repo.get_by_id(subtask_id)
        if not subtask:
            raise SubtaskNotFoundException()

        max_position = await self.subtask_repo.get_max_position(subtask.task_id)
        new_position = payload.position
        old_position = subtask.position

        # Validasi: posisi harus dalam range yang valid dan tidak sama
        if new_position < 1 or new_position > max_position or new_position == old_position:
            raise InvalidSubtaskPositionException()

        if new_position < old_position:
            # Subtask naik ke atas: geser subtask di antara [new_pos, old_pos-1] turun +1
            await self.subtask_repo.shift_positions(
                task_id=subtask.task_id,
                from_position=new_position,
                to_position=old_position - 1,
                shift=+1
            )
        else:
            # Subtask turun ke bawah: geser subtask di antara [old_pos+1, new_pos] naik -1
            await self.subtask_repo.shift_positions(
                task_id=subtask.task_id,
                from_position=old_position + 1,
                to_position=new_position,
                shift=-1
            )

        # Set posisi baru untuk subtask yang dipindah
        updated_subtask = await self.subtask_repo.update(
            subtask_id, {"position": new_position}
        )

        return SubtaskMoveResponse.model_validate(updated_subtask)
    
    async def delete_subtask(self, subtask_id: uuid.UUID) -> None:
        subtask = await self.subtask_repo.get_by_id(subtask_id)
        if not subtask:
            raise SubtaskNotFoundException()
 
        deleted_position = subtask.position
        task_id = subtask.task_id
 
        await self.subtask_repo.soft_delete(subtask_id)
 
        # Rapikan posisi: geser semua subtask di bawah posisi yang dihapus naik -1
        max_position = await self.subtask_repo.get_max_position(task_id)
        if deleted_position <= max_position:
            await self.subtask_repo.shift_positions(
                task_id=task_id,
                from_position=deleted_position + 1,
                to_position=max_position + 1,  # +1 karena max sudah dihitung tanpa yang dihapus
                shift=-1
            )