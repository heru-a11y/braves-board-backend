# type: ignore
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.task_repository import TaskRepository
from app.repositories.column_repository import ColumnRepository
from app.schemas.task import (
    TaskCreateRequest, TaskCreate, TaskDetailResponse,
    TaskUpdateRequest, TaskMoveRequest, TaskMoveResponse,
    TaskReorderRequest, TaskReorderResponse,
)
from app.exceptions.task_exceptions import (
    ColumnNotFoundException, TaskNotFoundException,
    InvalidTargetColumnException, InvalidTaskPositionException,
)
from app.constants import task_messages

class TaskService:
    @staticmethod
    async def create_task(db: AsyncSession, request: TaskCreateRequest):
        column_repo = ColumnRepository(db)
        column = await column_repo.get_by_id(request.column_id)

        if not column:
            raise ColumnNotFoundException()

        task_repo = TaskRepository(db)
        existing_tasks = await task_repo.get_all_by_column_id(request.column_id)

        new_position = len(existing_tasks) + 1

        task_data = TaskCreate(
            **request.model_dump(),
            position=new_position
        )

        return await task_repo.create(task_data)

    @staticmethod
    async def get_tasks_by_column(db: AsyncSession, column_id: uuid.UUID):
        column_repo = ColumnRepository(db)
        column = await column_repo.get_by_id(column_id)

        if not column:
            raise ColumnNotFoundException()

        task_repo = TaskRepository(db)
        records = await task_repo.get_all_by_column_id_with_counts(column_id)

        return [
            {
                "id": task.id,
                "title": task.title,
                "position": task.position,
                "due_date": task.due_date,
                "labels": task.labels,
                "assignee_ids": task.assignee_ids,
                "comment_count": comment_count,
                "attachment_count": attachment_count,
                "is_timer_running": task.is_timer_running
            }
            for task, comment_count, attachment_count in records
        ]

    @staticmethod
    async def get_task_detail(db: AsyncSession, task_id: uuid.UUID):
        task_repo = TaskRepository(db)
        task = await task_repo.get_detail_by_id(task_id)

        if not task:
            raise TaskNotFoundException()

        return TaskDetailResponse.model_validate(task).model_dump(mode='json')

    @staticmethod
    async def update_task(db: AsyncSession, task_id: uuid.UUID, request: TaskUpdateRequest):
        task_repo = TaskRepository(db)
        update_data = request.model_dump(exclude_unset=True)

        updated_task = await task_repo.update(task_id, update_data)

        if not updated_task:
            raise TaskNotFoundException()

        return {
            "id": updated_task.id,
            "updated_at": updated_task.updated_at
        }

    @staticmethod
    async def move_task(db: AsyncSession, task_id: uuid.UUID, request: TaskMoveRequest):
        task_repo = TaskRepository(db)
        column_repo = ColumnRepository(db)

        task = await task_repo.get_by_id(task_id)
        if not task:
            raise TaskNotFoundException()

        target_column = await column_repo.get_by_id(request.column_id)
        if not target_column:
            raise InvalidTargetColumnException()

        new_position = request.position
        source_column_id = task.column_id
        old_position = task.position

        target_max = await task_repo.get_max_position(request.column_id)
        is_same_column = source_column_id == request.column_id

        if is_same_column:
            if new_position < 1 or new_position > target_max or new_position == old_position:
                raise InvalidTaskPositionException()
        else:
            if new_position < 1 or new_position > target_max + 1:
                raise InvalidTaskPositionException()

        if is_same_column:
            if new_position < old_position:
                await task_repo.shift_positions(
                    column_id=source_column_id,
                    from_position=new_position,
                    to_position=old_position - 1,
                    shift=+1
                )
            else:
                await task_repo.shift_positions(
                    column_id=source_column_id,
                    from_position=old_position + 1,
                    to_position=new_position,
                    shift=-1
                )
        else:
            source_max = await task_repo.get_max_position(source_column_id)
            if old_position < source_max:
                await task_repo.shift_positions(
                    column_id=source_column_id,
                    from_position=old_position + 1,
                    to_position=source_max,
                    shift=-1
                )

            if new_position <= target_max:
                await task_repo.shift_positions(
                    column_id=request.column_id,
                    from_position=new_position,
                    to_position=target_max,
                    shift=+1
                )

        updated_task = await task_repo.update(task_id, {
            "column_id": request.column_id,
            "position": new_position
        })

        return TaskMoveResponse.model_validate(updated_task)

    @staticmethod
    async def reorder_task(db: AsyncSession, task_id: uuid.UUID, request: TaskReorderRequest):
        task_repo = TaskRepository(db)

        task = await task_repo.get_by_id(task_id)
        if not task:
            raise TaskNotFoundException()

        max_position = await task_repo.get_max_position(task.column_id)
        new_position = request.position
        old_position = task.position

        if new_position < 1 or new_position > max_position or new_position == old_position:
            raise InvalidTaskPositionException()

        if new_position < old_position:
            await task_repo.shift_positions(
                column_id=task.column_id,
                from_position=new_position,
                to_position=old_position - 1,
                shift=+1
            )
        else:
            await task_repo.shift_positions(
                column_id=task.column_id,
                from_position=old_position + 1,
                to_position=new_position,
                shift=-1
            )

        updated_task = await task_repo.update(task_id, {"position": new_position})

        return TaskReorderResponse.model_validate(updated_task)

    @staticmethod
    async def delete_task(db: AsyncSession, task_id: uuid.UUID):
        task_repo = TaskRepository(db)
        is_deleted = await task_repo.soft_delete(task_id)

        if not is_deleted:
            raise TaskNotFoundException()

        return {
            "message": task_messages.TASK_DELETED_SUCCESS
        }