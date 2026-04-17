import uuid
from datetime import datetime, timezone, timedelta

from fastapi import HTTPException

from app.core.redis import redis_client
from app.repositories.task_repository import TaskRepository
from app.repositories.time_log_repository import TimeLogRepository
from app.schemas.time_log_schemas import TimeLogCreate
from app.constants.time_tracking_messages import TimerMessage, TimerErrorMessage


class TaskTimerService:
    def __init__(self, task_repo: TaskRepository, time_log_repo: TimeLogRepository):
        self.task_repo = task_repo
        self.time_log_repo = time_log_repo

    def _get_key(self, task_id: uuid.UUID):
        return f"task:{task_id}:timer"

    async def start_timer(self, task_id: uuid.UUID, description: str | None = None):
        task = await self.task_repo.get_by_id(task_id)

        if not task:
            raise HTTPException(status_code=404, detail=TimerErrorMessage.TASK_NOT_FOUND)

        if task.is_timer_running:
            raise HTTPException(status_code=400, detail=TimerErrorMessage.TIMER_ALREADY_RUNNING)

        now = datetime.now(timezone.utc)
        key = self._get_key(task_id)

        await redis_client.hset(key, mapping={
            "start_time": now.isoformat(),
            "last_ping": now.isoformat(),
            "last_confirm": now.isoformat(),
            "description": description or ""
        })

        await self.time_log_repo.create(TimeLogCreate(
            task_id=task_id,
            start_time=now,
            activity_description=description
        ))

        await self.task_repo.update(task_id, {
            "is_timer_running": True,
            "start_time": now
        })

        return {
            "message": TimerMessage.STARTED,
            "data": {
                "task_id": str(task_id),
                "start_time": now,
                "description": description
            }
        }

    async def stop_timer(self, task_id: uuid.UUID):
        task = await self.task_repo.get_by_id(task_id)

        if not task:
            raise HTTPException(status_code=404, detail=TimerErrorMessage.TASK_NOT_FOUND)

        if not task.is_timer_running:
            raise HTTPException(status_code=400, detail=TimerErrorMessage.TIMER_NOT_RUNNING)

        key = self._get_key(task_id)
        data = await redis_client.hgetall(key)

        if not data:
            raise HTTPException(status_code=400, detail=TimerErrorMessage.TIMER_STATE_LOST)

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
            "message": TimerMessage.STOPPED,
            "data": {
                "task_id": str(task_id),
                "duration_added": duration,
                "total_duration": new_total,
                "stopped_at": now
            }
        }

    async def ping(self, task_id: uuid.UUID):
        key = self._get_key(task_id)
        data = await redis_client.hgetall(key)

        if not data:
            raise HTTPException(status_code=400, detail=TimerErrorMessage.TIMER_NOT_ACTIVE)

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
            return {"message": TimerMessage.AUTO_STOP_NO_ACTIVITY}

        if now - last_confirm > timedelta(minutes=10):
            await self.stop_timer(task_id)
            return {"message": TimerMessage.AUTO_STOP_NO_CONFIRM}

        await redis_client.hset(key, "last_ping", now.isoformat())

        return {
            "message": TimerMessage.PING_UPDATED,
            "data": {
                "task_id": str(task_id),
                "last_ping": now
            }
        }

    async def confirm(self, task_id: uuid.UUID):
        key = self._get_key(task_id)

        exists = await redis_client.exists(key)
        if not exists:
            raise HTTPException(status_code=400, detail=TimerErrorMessage.TIMER_NOT_ACTIVE)

        now = datetime.now(timezone.utc)

        await redis_client.hset(key, "last_confirm", now.isoformat())

        return {
            "message": TimerMessage.CONFIRMED,
            "data": {
                "task_id": str(task_id),
                "last_confirm": now
            }
        }

    async def get_time_logs(self, task_id: uuid.UUID):
        task = await self.task_repo.get_by_id(task_id)

        if not task:
            raise HTTPException(status_code=404, detail=TimerErrorMessage.TASK_NOT_FOUND)

        logs = await self.time_log_repo.get_all_by_task_id(task_id)

        return {
            "task_id": str(task_id),
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