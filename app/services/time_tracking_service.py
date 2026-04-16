import uuid
from datetime import datetime, timezone, timedelta

from fastapi import HTTPException
from app.core.redis import redis_client
from app.repositories.task_repository import TaskRepository
from app.repositories.time_log_repository import TimeLogRepository
from app.schemas.time_log_schemas import TimeLogCreate


class TaskTimerService:
    def __init__(self, task_repo: TaskRepository, time_log_repo: TimeLogRepository):
        self.task_repo = task_repo
        self.time_log_repo = time_log_repo

    def _get_key(self, task_id: uuid.UUID):
        return f"task:{task_id}:timer"

    async def start_timer(self, task_id: uuid.UUID):
        task = await self.task_repo.get_by_id(task_id)

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        if task.is_timer_running:
            raise HTTPException(status_code=400, detail="Timer already running")

        now = datetime.now(timezone.utc)
        key = self._get_key(task_id)

        await redis_client.hset(key, mapping={
            "start_time": now.isoformat(),
            "last_ping": now.isoformat(),
            "last_confirm": now.isoformat()
        })

        await self.time_log_repo.create(TimeLogCreate(
            task_id=task_id,
            start_time=now
        ))

        await self.task_repo.update(task_id, {
            "is_timer_running": True,
            "start_time": now
        })

        return {"message": "Timer started"}

    async def stop_timer(self, task_id: uuid.UUID):
        task = await self.task_repo.get_by_id(task_id)

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        if not task.is_timer_running:
            raise HTTPException(status_code=400, detail="Timer not running")

        key = self._get_key(task_id)
        data = await redis_client.hgetall(key)

        if not data:
            raise HTTPException(status_code=400, detail="Timer state lost")

        data = {
            (k.decode() if isinstance(k, bytes) else k):
            (v.decode() if isinstance(v, bytes) else v)
            for k, v in data.items()
        }

        start_time = datetime.fromisoformat(data["start_time"])
        if start_time.tzinfo is None:
            start_time = start_time.replace(tzinfo=timezone.utc)

        now = datetime.now(timezone.utc)

        duration = int((now - start_time).total_seconds())
        new_total = (task.total_duration or 0) + duration

        logs = await self.time_log_repo.get_all_by_task_id(task_id)
        if logs:
            last_log = logs[-1]

            if last_log.stop_time is None:
                await self.time_log_repo.update(last_log.id, {
                    "stop_time": now,
                    "duration_seconds": int((now - last_log.start_time).total_seconds())
                })

        await self.task_repo.update(task_id, {
            "is_timer_running": False,
            "start_time": None,
            "total_duration": new_total
        })

        await redis_client.delete(key)

        return {
            "message": "Timer stopped",
            "duration_added": duration,
            "total_duration": new_total
        }

    async def ping(self, task_id: uuid.UUID):
        key = self._get_key(task_id)
        data = await redis_client.hgetall(key)

        if not data:
            raise HTTPException(status_code=400, detail="Timer not active")

        data = {
            (k.decode() if isinstance(k, bytes) else k):
            (v.decode() if isinstance(v, bytes) else v)
            for k, v in data.items()
        }

        now = datetime.now(timezone.utc)

        last_ping = datetime.fromisoformat(data["last_ping"])
        if last_ping.tzinfo is None:
            last_ping = last_ping.replace(tzinfo=timezone.utc)

        last_confirm = datetime.fromisoformat(data["last_confirm"])
        if last_confirm.tzinfo is None:
            last_confirm = last_confirm.replace(tzinfo=timezone.utc)

        if now - last_ping > timedelta(minutes=5):
            await self.stop_timer(task_id)
            return {"message": "Auto stopped: no activity"}

        if now - last_confirm > timedelta(minutes=10):
            await self.stop_timer(task_id)
            return {"message": "Auto stopped: no confirmation"}

        await redis_client.hset(key, "last_ping", now.isoformat())

        return {"message": "Ping updated"}

    async def confirm(self, task_id: uuid.UUID):
        key = self._get_key(task_id)

        exists = await redis_client.exists(key)
        if not exists:
            raise HTTPException(status_code=400, detail="Timer not active")

        now = datetime.now(timezone.utc)

        await redis_client.hset(key, "last_confirm", now.isoformat())

        return {"message": "User confirmed activity"}

    async def get_time_logs(self, task_id: uuid.UUID):
        task = await self.task_repo.get_by_id(task_id)

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        logs = await self.time_log_repo.get_all_by_task_id(task_id)

        return {
            "task_id": task_id,
            "count": len(logs),
            "logs": [
                {
                    "id": str(log.id),
                    "start_time": log.start_time,
                    "stop_time": log.stop_time,
                    "duration_seconds": log.duration_seconds,
                    "created_at": log.created_at,
                    "activity_description": log.activity_description
                }
                for log in logs
            ]
        }
