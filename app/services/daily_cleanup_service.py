from datetime import datetime, timezone, timedelta
import json

from app.core.redis import redis_client
from app.constants.cleanup_messages import TIMER_KEY_PATTERN, MAX_INACTIVE_SECONDS, MAX_SESSION_SECONDS


class CleanupService:
    def __init__(self, task_repo, time_log_repo):
        self.task_repo = task_repo
        self.time_log_repo = time_log_repo

    async def run_cleanup(self):
        keys = await redis_client.keys(TIMER_KEY_PATTERN)

        now = datetime.now(timezone.utc)

        cleaned = 0
        stopped = []

        for key in keys:
            data = await redis_client.get(key)
            if not data:
                continue

            session = json.loads(data)

            last_ping = datetime.fromisoformat(session.get("last_ping"))
            start_time = datetime.fromisoformat(session.get("start_time"))
            task_id = session.get("task_id")
            user_id = session.get("user_id")

            inactive_duration = (now - last_ping).total_seconds()
            total_duration = (now - start_time).total_seconds()

            should_stop = (
                inactive_duration > MAX_INACTIVE_SECONDS
                or total_duration > MAX_SESSION_SECONDS
            )

            if should_stop:
                await self._force_stop(task_id, user_id, start_time, now)
                await redis_client.delete(key)

                cleaned += 1
                stopped.append(task_id)

        return {
            "cleaned_sessions": cleaned,
            "stopped_tasks": stopped
        }

    async def _force_stop(self, task_id, user_id, start_time, stop_time):
        await self.time_log_repo.create({
            "task_id": task_id,
            "user_id": user_id,
            "start_time": start_time,
            "stop_time": stop_time,
            "is_forced": True
        })