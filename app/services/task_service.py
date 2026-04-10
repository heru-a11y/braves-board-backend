# type: ignore
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.task_repository import TaskRepository
from app.repositories.column_repository import ColumnRepository
from app.schemas.task import TaskCreateRequest, TaskCreate, TaskDetailResponse, TaskUpdateRequest, TaskMoveRequest
from app.exceptions.task_exceptions import ColumnNotFoundException, TaskNotFoundException, InvalidTargetColumnException

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
        
        # Cek ketersediaan task
        task = await task_repo.get_by_id(task_id)
        if not task:
            raise TaskNotFoundException()

        # Cek validitas kolom tujuan
        target_column = await column_repo.get_by_id(request.column_id)
        if not target_column:
            raise InvalidTargetColumnException()

        # Ambil tugas yang sudah ada di kolom tujuan untuk menentukan posisi baru
        existing_tasks = await task_repo.get_all_by_column_id(request.column_id)
        new_position = len(existing_tasks) + 1

        update_data = {
            "column_id": request.column_id,
            "position": new_position
        }
        
        updated_task = await task_repo.update(task_id, update_data)

        return {
            "id": updated_task.id,
            "column_id": updated_task.column_id
        }