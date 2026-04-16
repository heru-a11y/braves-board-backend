import uuid
from datetime import datetime
from typing import Mapping, Any
from redis.asyncio.client import Redis
from app.schemas.redis_timer_schemas import ActiveTimerRedis

class RedisTimerRepository:
    def __init__(self, redis_client: Redis):
        self.redis = redis_client

    def _get_key(self, task_id: uuid.UUID) -> str:
        return f"active_timer:{str(task_id)}"

    async def set_active_timer(self, task_id: uuid.UUID, timer_data: ActiveTimerRedis) -> None:
        key = self._get_key(task_id)
        timer_mapping: Mapping[Any, Any] = {
            "start_time": timer_data.start_time.isoformat(),
            "last_ping_at": timer_data.last_ping_at.isoformat(),
            "last_confirmed_at": timer_data.last_confirmed_at.isoformat()
        }
        await self.redis.hset(key, mapping=timer_mapping)

    async def get_active_timer(self, task_id: uuid.UUID) -> ActiveTimerRedis | None:
        key = self._get_key(task_id)
        data = await self.redis.hgetall(key)
        
        if not data:
            return None

        data = {k.decode(): v.decode() for k, v in data.items()}  # 🔥 FIX

        return ActiveTimerRedis(
            start_time=datetime.fromisoformat(data["start_time"]),
            last_ping_at=datetime.fromisoformat(data["last_ping_at"]),
            last_confirmed_at=datetime.fromisoformat(data["last_confirmed_at"]),
            waiting_confirmation=data.get("waiting_confirmation", "false") == "true"
        )

    async def update_ping(self, task_id: uuid.UUID, ping_time: datetime) -> None:
        key = self._get_key(task_id)
        await self.redis.hset(key, "last_ping_at", ping_time.isoformat())

    async def update_confirmed(self, task_id: uuid.UUID, confirmed_time: datetime) -> None:
        key = self._get_key(task_id)
        await self.redis.hset(key, "last_confirmed_at", confirmed_time.isoformat())

    async def delete_active_timer(self, task_id: uuid.UUID) -> None:
        key = self._get_key(task_id)
        await self.redis.delete(key)